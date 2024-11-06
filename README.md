# Task Management

## Overview 

Building a simple Task Management API that allows users to
create, update, delete, and view tasks. Each task has a title, description, due date,
and status. Users should be able to filter tasks by their status (e.g., "Pending,"
"Completed").


My tech task:
- Django Rest Framework.

Reson to choose Django Rest Framework:
- Give me some powerful feature: Serialization, Authentication and Permissions, Viewsets and Routers, Filtering, Ordering, Pagination
- Rapid Development: Convention Over Configuration
- Integration with Django: integrates with Django's ORM and other features, making it easy to build complex APIs based on your existing Django models.
- Support powerful unit test

Overview my solution:

Using Django Rest Framework with template(Model-View):
- Where "View" is place receive the request from client
- Where "Model" interact with data of client to database

Structure my code:
- /customore/customre/: is place store common code like: base_api_view, setting for all project, etc
- /customore/task: is place store app task: all the logic of task management is store in here
  - /views: where to endpoint of api. Mission of this package: Receive and Response data to client
  - /services: where store logic handling database transaction and reponse to views
  - /exceptions: where store exceptions use for Task App
  - /migrations: use to store migrate file
  - /tests: use to store unit test of service and unit test of view
  - /enums: use to store enums use for Task App. For example: Response_code, Task Status
 


## Run My Code
First install requirement.txt by using this command
```
pip install requirement.txt
```
Set up database

- Please go docker-compose.yml to edit your username and password
- Edit setting on this path: /customore/customore/setting_template
  - Modify with approviate variable
  - change the namefolder of setting: setting_template -> setting 
- Run this command

```
docker-compose -f {compose file name} up
```

Migrate to create Schema
- Makemigrations use this command
```
python manage.py makemigrations 
```
- Migrate it to Databse
```
python manage.py migrate
```

Create User For Login
```
python manage.py createsuperuser

```


- Start Server
```
python manage.py runserver
```

## Run API
List of API:
- get-task/{task_id}
- create-task
- get-list-task
  - get-list-task/<limit_per_page>/<which_page>/<status_task>
  - get-list-task/<limit_per_page>/<page>
- update-task/{task_id}

Import Customore.postman_collection to your Postman

If you need to call another API, you first need run API:Login to get the Token

Input Data in request body to create-task or update-task

As you can see i dont use restful api, just use rest api(GET and POST). The reason i choose this, it make clear for debug api and easy to maintain than RESTFUL API.

## Run Unit Test

It will make sure another update of service or views. will run correctly


```
python manage.py test task.tests
```


## Improvement 

Base on some bussiness, will be improve performance by using: index or cache data.

For example:
  - Will mark index on id of task to query faster.
  - Cache favourite task of user to get faster on Redis
  - Use factory to generate random fake data will make sure all function run correctly
