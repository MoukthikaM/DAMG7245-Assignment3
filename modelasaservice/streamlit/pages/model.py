import streamlit as st
import json
import requests


st.title("Model As a Service")


backend = "http://fastapi:8000/uploadfile"
def process(vis,ir069,vil,ir107,server_url: str):

    # print(st.session_state['auth_code'])
    files=[('files',(vis.name,vis,'image/png')),('files',(ir069.name,ir069,'image/png')),('files',(vil.name,vil,'image/png')),('files',(ir107.name,ir107,'image/png'))]
    headers = {
  'Authorization': 'Bearer '+ st.session_state['auth_code']
}
    r = requests.post(
        server_url, files=files, headers=headers, timeout=8000
    )

    return r



def model_clicked():
        input_vis = st.file_uploader("insert vis")  # image upload widget
        input_vil = st.file_uploader("insert vil")  # image upload widget
        input_ir069 = st.file_uploader("insert ir069")  # image upload widget
        input_ir107 = st.file_uploader("insert ir107")  # image upload widget
        if st.button("Flashes ⛈️",key="flashes"):
             
            col1, col2 = st.columns(2)

            if input_vis and input_vil and input_ir069 and input_ir107:
             print("All images uploaded")
             
             st.balloons()
             segments = process(input_vis,input_ir069,input_vil,input_ir107,backend)
             flashes=segments.json()
             print(segments.json())
             col1.header("Flashes")
             col1.write(flashes['flashes'])
            else:
        # handle case with no image
             st.error("Insert all images please!")
logOutSection=st.container()
def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False
    st.session_state['auth_code'] = ""
    st.session_state['user'] = ""
    
def show_logout_page():
    with logOutSection:
        st.button ("Log Out", key="logout", on_click=LoggedOut_Clicked)


if 'auth_code' not in st.session_state:
    st.write("Please Login")

elif st.session_state["auth_code"]:
     model_clicked()
     show_logout_page()
else:
     st.write("Please Login")


