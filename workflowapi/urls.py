from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from workflowapi.views import initiate_workflow, get_workflow_details, get_workflow_task_details

urlpatterns = [
    url(r'^workflow/$', csrf_exempt(initiate_workflow), name='initiate-workflow'),
    url(r'^workflow/(?P<workflow_instance_id>(.+))/$',
        get_workflow_details, name='workflow-details'),
    url(r'^workflow/(?P<workflow_instance_id>(.+))/task/(?P<task_log_id>(.+))$',
        get_workflow_task_details, name='workflow-task-details'),
]
