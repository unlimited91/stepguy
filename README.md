# StepGuy

> Tenant based State Management and Execution system.


# Table of Contents

1. [Project setup](https://github.com/unlimited91/stepguy#project-setup)
2. [Run project](https://github.com/unlimited91/stepguy#run)
3. [API Quick look](https://github.com/unlimited91/stepguy#api-quick-look)
4. [Deployment Guidlines](https://github.com/unlimited91/stepguy#deployment-guidlines)


# Project setup

* I am using in memory sqlite3 for now. It should be created as soon as you run migrate. Later will move it to Postgres.
* `brew install redis`
* `brew services start redis`

* Setup `stepguy` database 
    * `python manage.py migrate`


# Run

*  You should be in the stepguy folder. Now fire up a terminal
*  In one tab run the API server `python manage.py runserver 8888`
*  In another tab run the Execution Engine `sh bin/start-execution-engine`
 

## API Quick look
* [Workflow API Code](workflowapi/views.py)

     Initiate Workflow
     
     ```
     curl --location --request POST 'localhost:8888/workflow/' \
      --header 'X-APIKEY: 54abced1-18fa-46b6-b78c' \
      --header 'Content-Type: application/json' \
      --data-raw '{
      "workflow_namespace": "scale_compute",
      "inputs": {
          "database_engine": "postgres",
          "owner_id": "sayan-1234",
          "size": "100gb",
          "instance_id": "ami-12345",
          "workflowapi_url": "https://antman-api.com/",
          "nova_flavor_id": "chocolate"
       }
      }'
     ```
      
     Get Workflow details
     
     ```
     curl --location --request GET 'localhost:8888/workflow/b4a8083e-d495-4539-8da4-db9af8752d93' \
      --header 'X-APIKEY: 54abced1-18fa-46b6-b78c'      
     ```
     
     Get Step details
     
     ```
     curl --location --request GET 'localhost:8888/workflow/b4a8083e-d495-4539-8da4-db9af8752d93/task/6f510d25-60d5-42b0-bac0-e523f802c575' \
      --header 'X-APIKEY: 54abced1-18fa-46b6-b78c'
     ```
     
     Will add one more API for retry workflow
     
* [Workflow Admin](workflowops/admin.py)




