from fastapi import FastAPI, HTTPException
from deta import Deta
from auth import Auth
from user_model import AuthModel
from fastapi import FastAPI, File, UploadFile
from fastapi import FastAPI, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import numpy as np
from sklearn import preprocessing
import numpy as np
from fastapi import FastAPI,Form,Request
from PIL import Image
from typing import Union,List
import pickle
import pandas as pd
deta = Deta("b0sokbvu_LHs85pSKRsz9pd2NKPT9STuozjsvwHp9")
users_db = deta.Base('users')

app = FastAPI()
security = HTTPBearer()
auth_handler = Auth()


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

def predictflash(X_test):
      model = pickle.load(open('model.pkl','rb'))
      print(model)
      flashes=model.predict(X_test)
      print(flashes[0])
      return flashes[0]
import re
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
def checkemail(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False
@app.post("/signup")
def signup(user_details: AuthModel):
    if users_db.get(user_details.username) != None:
        return 'Account already exists'
    try:
      if checkemail(user_details.username):
        hashed_password = auth_handler.encode_password(user_details.password)
        # print("jj")
        user = {'key': user_details.username, 'password': hashed_password}
        return users_db.put(user)
      else:
        return "invalid username"
    except:
        error_msg = 'Failed to signup user'
        return error_msg

@app.post("/login")
def login(user_details: AuthModel):
    print("login")
    # print(user_details)
    # print("test")
    
    user = users_db.get(user_details.username)
    
    # print(user)
    if (user is None):
        return HTTPException(status_code=401, detail='Invalid username')
    if (not auth_handler.verify_password(user_details.password, user['password'])):
        return HTTPException(status_code=401, detail='Invalid password')
    
    token = auth_handler.encode_token(user['key'])
    # print(token)
    return {'token': token}

@app.get('/refresh_token')
def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    expired_token = credentials.credentials
    return auth_handler.refresh_token(expired_token)

@app.post('/secret')
def secret_data(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    if(auth_handler.decode_token(token)):
        return 'Top Secret data only authorized users can access this info'

@app.get('/notsecret')
def not_secret_data():
    return 'Not secret data'



@app.post("/uploadfile")
async def create_upload_file(credentials: HTTPAuthorizationCredentials = Security(security),
    files: List[UploadFile] = File(description="A file read as UploadFile",default=None),
):
    token = credentials.credentials
    if(auth_handler.decode_token(token)):
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


def filename_eventid(eventtype,eventid):

      df1=pd.read_csv('datasets/sevir/CATALOG.csv',low_memory=False)
      regex=eventtype+""+eventid
    # print(regex)
      df1=df1[df1.id.str.startswith(regex)]
      df1=df1['file_name']
      df1.drop_duplicates()
      return df1

@app.get("/getfiles/{event_id}")
def getfiles(event_id,credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    if(auth_handler.decode_token(token)):
      filenames = filename_eventid('S', event_id)
      return filenames


def number_of_events(event_name):
  df_VIS = pd.read_csv('datasets/sevir/VIS_stats_master.csv', low_memory=False)
  counts=df_VIS['event'].value_counts()[event_name]
  return counts.item()

#second function
@app.get("/eventcount/{event_name}")
def eventcount(event_name,credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    df_VIS = pd.read_csv('datasets/sevir/VIS_stats_master.csv', low_memory=False)
    if(auth_handler.decode_token(token)):
        if event_name not in df_VIS['event'].values:
            raise HTTPException(status_code=400, detail="EVENT NOT FOUND, PLEASE ENTER THE CORRECT EVENT")
        eventcount=number_of_events(event_name)
        return {'Event count': eventcount }


def get_description(column):
    df_VIS = pd.read_csv('datasets/sevir/VIS_stats_master.csv', low_memory=False)
    return df_VIS[column].describe()

#third function
@app.get("/desc/{column}")
def desc(column,credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    df_VIS = pd.read_csv('datasets/sevir/VIS_stats_master.csv', low_memory=False)
    if(auth_handler.decode_token(token)):
        if column not in list(df_VIS.columns):
            raise HTTPException(status_code=400, detail="COLUMN NOT FOUND, PLEASE ENTER THE CORRECT COLUMN NAME")
        col_desc = get_description(column)
        return col_desc


from datetime import datetime as dt
import json
def convert(date_time):
    format = '%Y-%m-%d'  # The format
    datetime_str = dt.strptime(date_time, '%Y-%m-%d')
 
    return datetime_str
#fourth function
@app.get("/count/{Starting_Date}/{Ending_Date}")
def count_of_storms(Starting_Date,Ending_Date,credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    if(auth_handler.decode_token(token)):
        df1=pd.read_csv('datasets/sevir/CATALOG.csv',low_memory=False)
        df2=df1.loc[df1['time_utc'] > Starting_Date]
        df3=df1.loc[df1['time_utc'] < Ending_Date]
        counts1=df2['event_type'].value_counts()
        counts2 = df3['event_type'].value_counts()
        counts =counts1 + counts2
        print(counts)
        result = counts.to_json()
        parsed = json.loads(result)
        return parsed


@app.get("/location/{event_type}/{x}/{y}")
def getlocation(event_type,x,y,credentials: HTTPAuthorizationCredentials = Security(security)):
#fetch coords by event type
 token = credentials.credentials
 if(auth_handler.decode_token(token)):
  x=float(x)
  y=float(y)
  df_cat = pd.read_csv('datasets/sevir/CATALOG.csv', low_memory=False)
# Select Rows Based on event type
  values=[event_type]
  filter1 = df_cat.loc[df_cat["event_type"].isin(values)]
#select lat lons for that event type
  cols = [4,7,8,9,10,11,12]
  df_event_type = filter1[filter1.columns[cols]]
  df3 = df_event_type[(df_event_type['llcrnrlat'] < x) & (df_event_type['llcrnrlon'] < y) & (df_event_type['urcrnrlat'] > x) & (df_event_type['urcrnrlon'] > y)]
  if  df3.empty:
        raise HTTPException(status_code=400, detail="LOCATION NOT FOUND, PLEASE ENTER THE CORRECT COORDINATES AND EVENT TYPE")
  else :
        result = df3.to_json(orient="records")
        p = json.loads(result)
        
        return p
