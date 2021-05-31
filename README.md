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

*  Please install python3.7 and virtualenv for separation of python site packages.
*  You should be in the stepguy folder. Now fire up a terminal
*  Now create a virtual env in the folder. Don't worry it has been gitignored :) 
*  `virtualenv -p python3 venv` If you have only python3 and a symlink called python you can choose not to write `python3`
*  Now install packages `pip install -r requirements.txt`
*  In one tab run the API server `python manage.py runserver 8888`
*  In another tab run the Execution Engine `sh bin/start-execution-engine`
*  Now you should be able to see the homepage of Django admin at `localhost:8888/admin/`
*  Voila! Now you should be able upload workflows and initiate. But first you need a user
*  Fire up another terminal tab and run `python manage.py shell`
*  Do the following
*  `from django.contrib.auth.models import User`
*  `User.objects.create_superuser(username='admin', password='elon3.14', email='tesla@elongate.com')`
*  Now you should be able to log into `localhost:8888/admin/` with the following credentials.
*  Now upload a Workflow DSL file here `http://localhost:8888/admin/workflowops/workflowdsl/`
*  Today we only support YAML based configuration. You can take a look at an example (https://github.com/unlimited91/stepguy/tree/main/workflows/yaml/admin)
*  You should see an Action select box just above the Workflow DSL listing. Select the Action `Parse DSL file` from the select box and the system will start processing your YAML file.
*  Now you can start calling the below mentioned APIs
*  I have built the support for External Service Notifications moving a steo forward but haven't built it as an example. No time!! :) Will do it soonish
 

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




