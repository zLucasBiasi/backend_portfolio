
from users import *
from projects import *

from flask import Flask, request, jsonify

app = Flask (__name__)

@app.route('/', methods=['POST'])
def home():
  return {'message':'api do portfólio: biasiportfolio.vercel.app'}

@app.route('/create_user', methods=['POST'])
def create_new_user():
  data = request.get_json()
  
  email = data.get('email')
  password = data.get('password')
  name = data.get('name')

  try:
    jsonify('usuario criado com sucesso')

    return jsonify(create_user(email,password,name))

  except Exception as error:
    print('erro: ',error)

@app.route('/update_user', methods=['POST'])
def update_profile():
  data = request.get_json()

  token = data.get('token')
  email = data.get('email')
  password = data.get('password')
  name = data.get('name')
  
  return update_user(name,email,password,token)


@app.route('/login', methods=['POST'])
def login():
  
  data = request.get_json()

  email = data.get('email')
  password = data.get('password')

  if authenticate(email,password):
    token = authenticate(email,password)
   
    return jsonify({'message':'sucess','token':token})

  else:
    return jsonify({'message':'usuario ou senha invalidos'}),401

@app.route('/validate_token', methods=['POST'])
def validate():
  
  data = request.get_json()

  get_token_from_user = data.get('token')
  token_validated = validate_token(get_token_from_user)
  
  return jsonify(token_validated)

@app.route('/add_new_project', methods=['POST'])
def add_new_project_on_table():
  data = request.get_json()
  try:
      user = validate_token(data.get('token'))
      if user['email']:
        projects = add_project(data)

        return jsonify(projects)
  except:
    return {'message':'usuario não autorizado'}

app.run(port=5000, debug=False)