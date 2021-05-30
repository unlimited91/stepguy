# StepGuy

> Tenant based State Management and Execution system.


# Table of Contents

1. [API Quick look](https://github.com/unlimited91/stepguy#api-quick-look)
2. [Project setup](https://github.com/unlimited91/stepguy#project-setup)
3. [Run project](https://github.com/unlimited91/stepguy#run)
4. [Deployment Guidlines](https://github.com/unlimited91/stepguy#deployment-guidlines)


## API Quick look
* [Workflow API](workflowapi/views.py)
* [Workflow Admin](workflowops/admin.py)



# Project setup

* I am using in memory sqlite3 for now. It should be created as soon as you run migrate. Later will move it to Postgres.
* `brew install redis`
* `brew services start redis`

* Setup `stepguy` database 
    * `python manage.py migrate`
