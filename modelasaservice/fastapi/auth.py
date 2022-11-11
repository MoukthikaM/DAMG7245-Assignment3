import os
import jwt # used for encoding and decoding jwt tokens
from fastapi import HTTPException # used to handle error handling
from passlib.context import CryptContext # used for hashing the password 
from datetime import datetime, timedelta # used to handle expiry time for tokens

class Auth():
    hasher= CryptContext(schemes=["bcrypt"], deprecated="auto")
   #secret = os.getenv("APP_SECRET_STRING")
    secret = "8f728f7c7d4b894b702d10f2839bb92f296daf20b67278193b347004ec8de72a"
    def encode_password(self, password):
        print(type(password))
        return self.hasher.hash(password)

    def verify_password(self, password, encoded_password):
        return self.hasher.verify(password, encoded_password)
    
    def encode_token(self, username):
        print(type(username))        
        payload = {
            'exp' : datetime.utcnow() + timedelta(days=0, minutes=30),
            'iat' : datetime.utcnow(),
            'sub' : username
        }

        return jwt.encode(
            payload, 
            self.secret,
            algorithm='HS256'
        )
    
    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')
    
    def refresh_token(self, expired_token):
        try:
            payload = jwt.decode(expired_token, self.secret, algorithms=['HS256'], options= {'verify_exp': False})
            username = payload['sub']
            new_token = self.encode_token(username)
            return {'token': new_token}
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')
