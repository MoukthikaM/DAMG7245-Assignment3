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
        # print(response.text)
        dict=json.loads(response.text)
        print(dict)
        if 'key' not in dict:
                return False,dict
        else :
                return True,dict


username = st.text_input("User Name")
password = st.text_input("Password",type='password')

if st.button('SignUp'):    
    if username and password:        
        result,dict=signup_user(username,password)
        # print(result)
        if result:
            st.success("You have successfully created an account.Go to the Login Menu to login")
        elif dict=='invalid username': 
            st.error("Enter Valid Email")
        else: 
            st.error("Signup Failed username already present")
    else:
         st.error("Please Fill the Details")   
        
