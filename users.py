import os
from dotenv import load_dotenv

import jwt
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGO_AUTH"))

db = client['users']

def create_user(email,password,name):
    db.data_users.insert_one({"email":email,"password":password,"name":name})
    return {}

def update_user(name,email,password,token):
    try:
        user = validate_token(token)
        if user['email']:
            myquery = { "email": user['email'] }
            newvalues = { "$set": { "email":email, "password": password,"nome":name } }

            db.data_users.update_one(myquery, newvalues)

            payload = {
                'email': email,
                'password': password 
                }
            secret = "key_super_secreta_confia"

            token = jwt.encode(payload,secret,algorithm='HS256')
            
            return {'token':token,'message':'usuario atualizado com sucesso'}
        else:
            raise
    except :
        return {'message':'token invalido'}


def authenticate(email, password):
    user = db.data_users.find_one({"email":email,"password":password})
    if user:
        payload = {
                'email': user['email'],
                'password': user['password'],
            }
        secret = "key_super_secreta_confia"

        token = jwt.encode(payload,secret,algorithm='HS256')
        
        return token
    return False

def show_user(email,password):
    user = db.data_users.find_one({"email":email,"password":password})
    if user:
        usuario = {"email":user['email'],"name":user['name']}
        return  usuario
    return False

def validate_token(token):
    secret = "key_super_secreta_confia"
    data = jwt.decode(token, key=secret, algorithms=['HS256'])

    return show_user(data["email"],data["password"])