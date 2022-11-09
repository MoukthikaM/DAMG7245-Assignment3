from email.policy import default
import numpy as np
from sklearn import preprocessing
import numpy as np
from fastapi import FastAPI,Form,Request
from PIL import Image
from typing import Union,List
import pickle

app = FastAPI()

from pydantic import BaseModel

class Images(BaseModel):
    vis: str
    vil: str
    ir069: str
    ir107: str

import io
def imagepreprocessing(image):
    # path='../'+events+'.png'
    # print(path)
    im_gray = np.array(Image.open(io.BytesIO(image)))
    print(im_gray.shape)
    # im_gray = np.array(Image.open(path),np.float64)
    percent=percentile(preprocessing.normalize(im_gray*1e-4))
    print((percent))
    print(im_gray.shape)
    return percent



def percentile(data_sub):
   desired_percentiles = np.array([0,1,10,25,50,75,90,99,100])
   percentiles = np.nanpercentile(data_sub,desired_percentiles,axis=(0,1))
   percentiles = np.reshape(percentiles, (1, -1))
   return percentiles







@app.post("/flashes")
async def flashes(images: Images):
    vis = imagepreprocessing(images.vis)
    ir069 = imagepreprocessing(images.ir069)
    ir107 = imagepreprocessing(images.ir107)
    vil = imagepreprocessing(images.vil)
    X_test=np.concatenate((ir107,ir069,vis,vil),axis=1)
    print(X_test.shape)
    flashes = predictflash((X_test))
    return {'flashes': flashes}




def predictflash(X_test):
      model = pickle.load(open('model.pkl','rb'))
      print(model)
      flashes=model.predict(X_test)
      print(flashes[0])
      return flashes[0]

from fastapi import FastAPI, File, UploadFile

@app.post("/images")
async def create_upload_file(request: Request ):
    file = request.files["file"]
    return {"filename": file.filename}


@app.post("/test")
def get_test(files: List[UploadFile] = File( ...)):
    print(type(files))
    for f in files:
        print(f)
    # vis = imagepreprocessing(file)
    # print(vis.shape)
    # X_test=np.concatenate((vis,vis,vis,vis),axis=1)
    # print(X_test.shape)
    # flashes = predictflash((X_test))
    # return {'flashes': flashes}
    # segmented_image.save(bytes_io, format="PNG")
    # return Response(bytes_io.getvalue(), media_type="image/png")
    return "ok"
 

@app.post("/uploadfile")
async def create_upload_file(
    files: List[UploadFile] = File(description="A file read as UploadFile",default=None),
):
    contents=[]
    print([file.filename for file in files])
    for f in files:
        content = await f.read()
        contents.append(content)
    vis = imagepreprocessing(contents[0])
    ir069 = imagepreprocessing(contents[1])
    vil = imagepreprocessing(contents[2])
    ir107 = imagepreprocessing(contents[3])
    print(vis.shape)
    X_test=np.concatenate((ir107,ir069,vis,vil),axis=1)
    print(X_test.shape)
    flashes = predictflash((X_test))
    return {'flashes': flashes}



