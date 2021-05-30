from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_GET, require_POST

from utils.helpers import JsonNotFoundResponse, JsonOKResponse, JsonBadRequestResponse, JsonNotPermittedResponse
from workflowapi.helpers import validate_input_dictionary
from workflowapi.models import WorkflowInstance, TaskLogs
from workflowapi.tasks import InitiatePendingWorkflow
from workflowops.models import Workflow, Task
import json


@require_POST
def initiate_workflow(request):
    request_body = json.loads(request.body)
    workflow_namespace = request_body['workflow_namespace']
    input_dictionary = request_body['inputs']
    try:
        workflow = Workflow.objects.get(workflow_namespace=workflow_namespace)
        if not request.user == workflow.user:
            return JsonNotPermittedResponse(data={'msg': 'This is not your creds buddy!!!!'})
        validate_input_dictionary(workflow.inputs, input_dictionary)
        workflow_instance = WorkflowInstance.objects.create(
            workflow=workflow,
            user=request.user,
            inputs=workflow.inputs,
            context=input_dictionary
        )
        InitiatePendingWorkflow.delay(workflow_instance.pk)
    except ValidationError:
        return JsonBadRequestResponse(data={'msg': 'Incorrect workflow inputs'})
    except Workflow.DoesNotExist:
        return JsonNotFoundResponse()
    return JsonOKResponse(
        data={
            'workflow_instance_id': workflow_instance.pk,
            'status': workflow_instance.status,
            'msg': 'Successful'
        }
    )


@require_GET
def get_workflow_details(request, workflow_instance_id):
    try:
        workflow_instance = WorkflowInstance.objects.get(pk=workflow_instance_id)
        if not request.user == workflow_instance.user:
            return JsonNotPermittedResponse(data={'msg': 'This is not your creds buddy!!!!'})
        response = {
            'workflow_instance_id': workflow_instance.pk,
            'status': workflow_instance.status,
            'msg': 'Successful'
        }

        task_logs = TaskLogs.objects.filter(
            task_id__in=workflow_instance.workflow.tasks.values_list('pk')).order_by('task__level')
        if task_logs.exists():
            task_jsons = []
            for task_log in task_logs:
                task_jsons.append(
                    {
                        'task_name': task_log.task.task_name,
                        'task_id': task_log.pk,
                        'status': task_log.status
                    }
                )
            response['tasks'] = task_jsons
    except WorkflowInstance.DoesNotExist:
        return JsonNotFoundResponse(data={'msg': 'Incorrect workflow instance'})
    return JsonOKResponse(data=response)


@require_GET
def get_workflow_task_details(request, workflow_instance_id: str, task_log_id: str):
    try:
        workflow_instance = WorkflowInstance.objects.get(pk=workflow_instance_id)
        if not request.user == workflow_instance.user:
            return JsonNotPermittedResponse(data={'msg': 'This is not your creds buddy!!!!'})
        state = TaskLogs.objects.get(pk=task_log_id)
        response = {
            'workflow_instance_id': workflow_instance.pk,
            'status': workflow_instance.status,
            'msg': 'Successful',
            'tasks': {
                'task_id': state.pk,
                'status': state.status,
                'request_body': state.request_body,
                'response_body': state.response_body
            }
        }
    except WorkflowInstance.DoesNotExist:
        return JsonNotFoundResponse(data={'msg': 'Incorrect workflow instance'})
    except TaskLogs.DoesNotExist:
        return JsonNotFoundResponse(data={'msg': 'Incorrect task id'})
    return JsonOKResponse(data=response)







