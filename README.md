# playvox-test

This repository contains test for playvox

The ui for this test is [here]( http://54.197.246.139:8000)

Stack
===
1. [Bottle](https://bottlepy.org/docs/dev/)
2. [Mongodb](https://www.mongodb.com/)
3. Python 3.7
4. [Docker](https://www.docker.com/)
5. [Docker-compose](https://docs.docker.com/compose/)
6. [Vuejs](https://vuejs.org/)

Installation
======

1. Clone repository 

``` 
git clone https://github.com/jonthdiaz/playvox-test.git
```
2. Install docker
3. Install docker-compose
4. Going to path where you clone the repository
5. Running the next command
```
docker-compose up -d 
```

After that you can go the url http://localhost:8000 to see the web ui


Api
======

### Create new user

It makes post to the url http://localhost:8010/v1/users

```javascript
Params 
name, lastname, age, gender, email, registration_date all these fields are required
```
### Delete user

It makes delete to the url http://localhost:8010/v1/users with "id" as data parameter

### Update user

It makes put to the url http://localhost:8010/v1/users with "id" as data parameter

```
Params
id, name, lastname, age, gender, email, registration_date
```

### Get user

It makes get to the url http://localhost:8010/v1/users/:id where id is the Object id of the user

### Create new user's note

It makes post to the url http://localhost:8011/v1/user/:id/notes where id is the Object id of the user
```
Params
id, title, body, created where id is the Object id of the user
```




