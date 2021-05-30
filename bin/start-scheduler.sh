#!/bin/bash

celery beat --app workflowmanager  -l info --schedule=/tmp/celerybeat-schedule.db --pidfile=/tmp/celerybeat.pid
