import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGO_AUTH"))

db = client['projects']

def add_project(props):
    try:
        if check_if_the_project_exists(props['name']) != 0:
            return {'message':'Já existe um projeto registrado com esse nome','error':True}
        
        db.data_projects.insert_one({"name":props['name'],"languages":props['languages'],"image":props['image'],"link":props['link']})

        return props

    except Exception as error:
        print(error)

def check_if_the_project_exists(name):
    return db.data_projects.count_documents({'name':name},limit = 1)

