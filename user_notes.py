from bottle import route, run, template, Bottle, response, request
import json
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps


client = MongoClient('mongodb://appuser:secret@db/playvox_user_notes?authSource=admin', 27017)
db = client.playvox_user_notes


client_users = MongoClient('mongodb://appuser:secret@db/playvox_users?authSource=admin', 27017)
db_users = client_users.playvox_users

app = Bottle()

@app.hook('after_request')
def enable_cors():
  """
  You need to add some headers to each request.
  Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
  """
  response.headers['Access-Control-Allow-Origin'] = '*'
  response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
  response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@app.post('/v1/user/:id/notes')
def user_create_notes(id):
  data = request.json or {}
  errors = []
  user_id = id
  title = data.get('title')
  body = data.get('body')
  created = data.get('created')
  
  if not user_id:
    errors.append('User is required')

  if not title:
    errors.append('Title is required')

  if not body:
    errors.append('Body is required')

  if not created:
    errors.append('Created is required')


  if not ObjectId.is_valid(user_id):
    return json.dumps('Id is invalid')

  if db_users.users.count({'_id': ObjectId(user_id)}) <= 0:
    return json.dumps('User does not exists')
    

  if len(errors) > 0:
    response.content_type = 'application/json'
    return json.dumps(errors)


  result = db.notes.insert_one({"user_id":user_id, "title":title, "body":body, 
                                "created":created})

  response.content_type = 'application/json'
  return json.dumps("Record created correctly %s" % str(result.inserted_id))

@app.get('/v1/user/:id/notes')
def user_get_notes(id):
  response.content_type = 'application/json'

  notes = db.notes.find({'user_id': id})
  return dumps(notes)


run(app, host='0.0.0.0', port=8011, debug=True, reloader=True)

