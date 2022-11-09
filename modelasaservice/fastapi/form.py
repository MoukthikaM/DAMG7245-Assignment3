from fastapi import FastAPI, File, UploadFile
from typing import List

app = FastAPI()


@app.post("/files/")
async def create_file(files: List[bytes] = File(description="A file read as bytes",default=None)):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfile/")
async def create_upload_file(
    files: List[UploadFile] = File(description="A file read as UploadFile",default=None),
):
    return {"filenames": [file.filename for file in files]}
