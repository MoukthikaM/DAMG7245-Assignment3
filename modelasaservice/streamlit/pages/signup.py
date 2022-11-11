import streamlit as st  
import json
import requests

st.session_state["auth_code"]=""
st.session_state['loggedIn'] = False
def signup_user(username,password):
       
        url = "http://fastapi:8000/signup"
        payload = json.dumps({
  "username": username,
  "password": password
})
        headers = {
  'Content-Type': 'application/json'
}

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        dict=json.loads(response.text)
        if 'key' not in dict:
                return False
        else :
                return True


username = st.text_input("User Name")
password = st.text_input("Password",type='password')

if st.button('SignUp'):        
        result=signup_user(username,password)
        print(result)
        if result:
            st.success("You have successfully created an account.Go to the Login Menu to login")
        else: 
            st.error("Signup Failed username already present")
 
        
