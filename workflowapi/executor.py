import abc
import json
import logging
import ast

import requests
from djchoices import DjangoChoices, ChoiceItem

from workflowapi.models import TaskLogs
from workflowops.models import Task


logger = logging.getLogger(__name__)


class ExecutorService:

    def __init__(self, strategy, task):
        self.strategy = strategy
        self.task = task

    def execute(self):
        return self.strategy.execute_strategy(self.task)


class StrategyResult(DjangoChoices):
    successful = ChoiceItem('SUCCESS', 'SUCCESS')
    failed = ChoiceItem('FAILED', 'FAILED')
    permanent_failure = ChoiceItem('PERMANENT_FAILURE', 'PERMANENT_FAILURE')
    unknown = ChoiceItem('UNKNOWN', 'UNKNOWN')


class BaseProtocolStrategy(abc.ABC):

    def execute_strategy(self, task):
        raise NotImplementedError()


class HTTPProtocolStrategy(BaseProtocolStrategy):

    def get_request_body(self, task):
        context = ast.literal_eval(task.state.workflow_instance.context)
        message_template = ast.literal_eval(task.action_message_template)
        for key, value in message_template.items():
            valuei = value.replace("<", "").replace(">", "")
            message_template[key] = context[valuei]
        return message_template

    def publish_data(self, task, response_body):
        response_dict = ast.literal_eval(response_body.content.decode('utf-8'))
        if response_dict:
            context = task.state.workflow_instance.context
            context = ast.literal_eval(context)
            # Updating the current context
            context.update(response_dict)
            task.state.workflow_instance.context = context
            task.state.workflow_instance.save()
            task.state.workflow_instance.refresh_from_db()

    def execute_strategy(self, task):
        """
        This function returns a Strategy Result
        """
        request_endpoint = task.action_endpoint
        if task.protocol_method == Task.MethodChoices.http_get:
            response = requests.get(url=request_endpoint)
        else:
            task.state.request_body = self.get_request_body(task)
            response = requests.post(url=request_endpoint, data=task.state.request_body)
        task.state.response_body = response
        task.state.request_endpoint = request_endpoint
        task.state.save()
        self.publish_data(task, response)
        if response.ok:
            logger.info(f"Task {task.task_name} with id {task.state.pk} completed")
            task.state.status = TaskLogs.Status.successful
            strategy_response = StrategyResult.successful
        elif task.state.no_of_tries == task.retry_count:
            logger.info(f"Task {task.task_name} with id {task.state.pk} permanently failed")
            task.state.status = TaskLogs.Status.permanently_failed
            strategy_response = StrategyResult.permanent_failure
        elif task.state.no_of_tries < task.retry_count:
            logger.info(f"Task {task.task_name} with id {task.state.pk} failed. This should be tried again")
            task.state.status = TaskLogs.Status.failed
            task.state.no_of_tries += 1
            strategy_response = StrategyResult.failed
        else:
            logger.info(f"Task {task.task_name} with id {task.state.pk} unknown")
            task.state.status = TaskLogs.Status.unknown
            strategy_response = StrategyResult.unknown
        task.state.save()
        return strategy_response


