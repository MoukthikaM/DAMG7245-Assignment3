import streamlit as st
import requests
import pandas as pd
import json
st.title("Data As a Service")


def postreq(path,params):
        url = "http://fastapi:8000/"+path+params
        print(url)
        payload={}
        headers = {
  'Authorization': 'Bearer '+st.session_state['auth_code']
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        # print(response.text)
        # print("here")
        return response.text

def data_clicked():
    if st.checkbox("GetFiles",key="GetFiles"):
           st.write("Enter Event ID")
           EventID = st.text_input (label="EventID", value="", placeholder="Enter Event ID")
           print(EventID)
           if st.button('result',key = 'one'):
                result=postreq("getfiles/",EventID)
                st.json(result)
    if st.checkbox("getEventCount",key="getEventCount"):
            st.write("files")
            EventName = st.text_input (label="EventName", value="", placeholder="Enter Event Name")
            print(EventName)
            if st.button('result',key = 'two'):
                result=postreq("eventcount/",EventName)
                st.json(result)
    if st.checkbox("getColumnDesc",key="getColumnDesc"):
            st.write("files")
            ColumnName = st.text_input (label="ColumnName", value="", placeholder="Enter Column Name")
            if st.button('result',key = 'three'):
                result=postreq("desc/",ColumnName)
                st.json(result)
    if st.checkbox("getEventcountTimePeriod",key="getEventcountTimePeriod"):
            st.write("files")
            Start = st.text_input (label="Start Date", value="", placeholder="Enter Start Date")
            End = st.text_input (label="End Date", value="", placeholder="Enter End Date")
            params=Start+"/"+End
            if st.button('result',key = 'four'):
                result=postreq("count/",params)
                st.json(result)
    if st.checkbox("getEventsByLocation",key="getEventsByLocation"):
            st.write("files")
            EventType = st.text_input (label="EventType", value="", placeholder="Enter EventType")
            Lat = st.text_input (label="Latitude", value="", placeholder="Enter Latitude")
            Long = st.text_input (label="Longitude", value="", placeholder="Longitude")
            params=EventType+"/"+Lat+"/"+Long
            if st.button('result',key = 'five'):
                result=postreq("location/",params)
                print(type(result))
                st.json(result)

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
     data_clicked()
     show_logout_page() 
else:
     st.write("Please Login")


