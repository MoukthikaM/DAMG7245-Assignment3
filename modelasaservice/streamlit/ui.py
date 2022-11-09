from email.mime import image
import io

import requests
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder

import streamlit as st
import fastapi as f
# interact with FastAPI endpoint
backend = "http://fastapi:8000/uploadfile"


def process(vis,ir069,vil,ir107,server_url: str):

    # m = MultipartEncoder(fields={"files": (vis.name, vis, "image/jpeg")})
    files=[('files',(vis.name,vis,'image/png')),('files',(ir069.name,ir069,'image/png')),('files',(vil.name,vil,'image/png')),('files',(ir107.name,ir107,'image/png'))]
    # "Content-Type": m.content_type
    r = requests.post(
        server_url, files=files, headers={}, timeout=8000
    )

    return r



def make_api_request(test_files,image):
    print("req")
    print(type(test_files))
    response = requests.post(backend, image ,headers={"Content-Type": "image/png"})
    if response.status_code != 200:
        return {
            'error': response.status_code,
            'message': response.text
        }
    else:
        return response.json() 

# construct UI layout
st.title("Regression for SEVIR data")

st.write(
    """  Upload images of all different types vis,vil,ir069,ir107
         This streamlit example uses a FastAPI service as backend.
         Visit this URL at `:8000/docs` for FastAPI documentation."""
)  # description and instructions

input_vis = st.file_uploader("insert vis")  # image upload widget
print(input_vis)
input_vil = st.file_uploader("insert vil")  # image upload widget
print(input_vil)
input_ir069 = st.file_uploader("insert ir069")  # image upload widget
print(input_ir069)
input_ir107 = st.file_uploader("insert ir107")  # image upload widget
print(input_ir107)
if st.button("Flashes"):
    print("ok")

    col1, col2 = st.columns(2)

    if input_vis and input_vil and input_ir069 and input_ir107:
         print("All images uploaded")
         print("xx")
         print(input_ir069)
         segments = process(input_vis,input_ir069,input_vil,input_ir107,backend)
        #  print(segments.json())
         flashes=segments.json()
         print(segments.json())
         col1.header("Flashes")
         col1.write(flashes['flashes'])
         

    else:
        # handle case with no image
        st.write("Insert all images please!")

