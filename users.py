from bottle import route, run, template, Bottle, response, request
import json
from pymongo import MongoClient
from bson.objectid import ObjectId


client = MongoClient('mongodb://appuser:secret@db/playvox_users?authSource=admin', 27017)
db = client.playvox_users

app = Bottle()

@app.post('/v1/users')
def user_create():
  data = request.json or {}
  errors = []
  name = data.get('name')
  lastname = data.get('lastname')
  age = data.get('age')
  gender = data.get('gender')
  email = data.get('email')
  registration_date = data.get('registration_date')
  
  if not name:
    errors.append('Name is required')

  if not lastname:
    errors.append('Lastname is required')

  if not age:
    errors.append('Age is required')

  if not gender:
    errors.append('Gender is required')

  if not email:
    errors.append('Email is quired')

  if not registration_date:
    errors.append('Registration date is required')

  if len(errors) > 0:
    response.content_type = 'application/json'
    return json.dumps(errors)

  if db.users.count({'name': name}) >= 0:  
    response.content_type = 'application/json'
    return json.dumps('User already exists')

  result = db.users.insert_one({"name":name, "lastname":lastname, "age":age, 
                                "gender":gender, "email":email, 
                                "registration_date":registration_date})

  response.content_type = 'application/json'
  return json.dumps("User created correctly %s" % str(result.inserted_id))


@app.delete('/v1/users')
def user_delete():
  response.content_type = 'application/json'
  data = request.json or {}
  user_id = data.get('id')
  
  if not user_id:
    return json.dumps('User does not exists')

  if not ObjectId.is_valid(user_id):
    return json.dumps('Id is invalid')


  if db.users.count({'_id': ObjectId(user_id)}) <= 0:
    return json.dumps('User does not exists')

  db.users.delete_one({'_id': ObjectId(user_id)})


  return json.dumps('User deleted correctly')

@app.put('/v1/users')
def user_update():
  response.content_type = 'application/json'
  data = request.json or {}
  user_id = data.get('id')
  fields_update = {}
  
  if not user_id:
    return json.dumps('User does not exists')

  if not ObjectId.is_valid(user_id):
    return json.dumps('Id is invalid')


  if db.users.count({'_id': ObjectId(user_id)}) <= 0:
    return json.dumps('User does not exists')

  name = data.get('name')
  lastname = data.get('lastname')
  age = data.get('age')
  gender = data.get('gender')
  email = data.get('email')
  registration_date = data.get('registration_date')
  
  if name:
    fields_update['name'] = name

  if lastname:
    fields_update['lastname'] = lastname

  if age:
    fields_update['age'] = age

  if gender:
    fields_update['gender'] = gender

  if email:
    fields_update['email'] = email

  if registration_date:
    fields_update['registration_date'] = registration_date


  for index in fields_update:
    db.users.update({'_id':ObjectId(user_id)}, {'$set': {index:fields_update[index]}})
  #

  return json.dumps('User update correctly')

@app.get('/v1/users/:id')
def single_user(id):
  response.content_type = 'application/json'
  user_id = id
  
  if not user_id:
    return json.dumps('User does not exists')

  if not ObjectId.is_valid(user_id):
    return json.dumps('Id is invalid')


  if db.users.count({'_id': ObjectId(user_id)}) <= 0:
    return json.dumps('User does not exists')
  
  user =  db.users.find_one({'_id': ObjectId(user_id)}, { '_id': 0 })
  
  return json.dumps(user)


@app.get('/v1/users')
def user():
  response.content_type = 'application/json'
  data = request.json or {}
  user_id = data.get('id')
  
  if not user_id:
    return json.dumps('User does not exists')

  if not ObjectId.is_valid(user_id):
    return json.dumps('Id is invalid')


  if db.users.count({'_id': ObjectId(user_id)}) <= 0:
    return json.dumps('User does not exists')
  
  user =  db.users.find_one({'_id': ObjectId(user_id)}, { '_id': 0 })
  
  return json.dumps(user)

run(app, host='0.0.0.0', port=8010, debug=True, reloader=True)
