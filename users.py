from bottle import route, run, template, Bottle, response, request
import json
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
import pymongo

client = MongoClient('mongodb://appuser:secret@db/playvox_users?authSource=admin', 27017)
db = client.playvox_users

app = Bottle()

#create index
db.users.create_index([('name', pymongo.TEXT)])

@app.hook('after_request')
def enable_cors():
  """
  You need to add some headers to each request.
  Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
  """
  response.headers['Access-Control-Allow-Origin'] = '*'
  response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
  response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

'''
  Method: Post
  Description: Create a new user in database
  Params: name, lastname, age, gender, email, registration_date all fields are required
'''
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

  if db.users.count({'name': name}) >= 1:  
    response.content_type = 'application/json'
    return json.dumps('User already exists')

  result = db.users.insert_one({"name":name, "lastname":lastname, "age":age, 
                                "gender":gender, "email":email, 
                                "registration_date":registration_date})

  response.content_type = 'application/json'
  return json.dumps("User created correctly %s" % str(result.inserted_id))

'''
  Method: delete
  Description: Remove user from db
  Params: User id 
'''
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

'''
  Method: Put
  Description: Update user's fields
  Params: name, lastname, age, gender, email, registration_date
'''
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


'''
  Method: Get
  Description: Get information about a user with user id in the url
  params: User id
'''
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


'''
  Method: Get
  Description: Get information about a user getting id from data
  params: User id
'''
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


'''
  Method: Get
  Description: Search information about user by name, lastname, agender and email
  Params: query, it is a string to search
'''
@app.get('/v1/users/search_by')
def user_search_by():
  response.content_type = 'application/json'
  query = request.query.get('query') 
  users = db.users.find({'$or': [{'name': {'$regex':query}},
                                 {'lastname': {'$regex':query}},
                                 {'gender': {'$regex':query}},
                                 {'email': {'$regex':query}},
                                ]})
  return dumps(users)


run(app, host='0.0.0.0', port=8010, debug=True, reloader=True)
