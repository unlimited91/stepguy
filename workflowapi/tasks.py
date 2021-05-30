import logging

from celery.task import Task as CeleryTask
from django.core.exceptions import ObjectDoesNotExist

from workflowapi.executor import ExecutorService, HTTPProtocolStrategy, StrategyResult
from workflowapi.models import WorkflowInstance, TaskLogs
from workflowops.models import Task

logger = logging.getLogger(__name__)


class ExecuteTaskState(CeleryTask):

    def run(self, workflow_instance_id, task_id):
        workflow_instance = WorkflowInstance.objects.get(pk=workflow_instance_id)
        if workflow_instance.status == WorkflowInstance.Status.completed:
            logger.info(f"Workflow {workflow_instance_id} already completed")
            return
        task = Task.objects.get(pk=task_id)
        state, _ = TaskLogs.objects.get_or_create(
            workflow_instance=workflow_instance,
            task=task
        )

        # Assigning in memory for ease. Maybe if it's not a good idea will remove it
        task.state = state
        if state.status == TaskLogs.Status.successful:
            return

        executor_service = ExecutorService(
            strategy=HTTPProtocolStrategy(),
            task=task
        )
        result = executor_service.execute()
        if result == StrategyResult.failed:
            # This delays the step to be retried
            logger.info(
                f"Task {task.task_name} with id {task.state.pk} failed. Will be retried with delay {task.delay}")
            ExecuteTaskState.apply_async(
                kwargs={
                    'workflow_instance_id': workflow_instance_id,
                    'task_id': task.pk
                }, countdown=task.delay)
        elif result in [StrategyResult.permanent_failure, StrategyResult.unknown]:
            logger.info(f"Notify Engineer regarding task state {task.state.pk}")


class InitiatePendingWorkflow(CeleryTask):

    def run(self, workflow_instance_id):
        logger.info("********************************************")
        logger.info(f"Starting the task with {workflow_instance_id}")
        workflow_instance = WorkflowInstance.objects.get(pk=workflow_instance_id)
        if workflow_instance.status == WorkflowInstance.Status.completed:
            logger.info(f"Workflow {workflow_instance_id} already completed")
            return
        tasks = Task.objects.filter(workflow=workflow_instance.workflow).order_by('level')
        for task in tasks:
            logger.info(f"Starting for task {task.task_name}")

            state, _ = TaskLogs.objects.get_or_create(
                workflow_instance=workflow_instance,
                task=task
            )

            # Assigning in memory for ease. Maybe if it's not a good idea will remove it
            task.state = state

            executor_service = ExecutorService(
                strategy=HTTPProtocolStrategy(),
                task=task
            )
            result = executor_service.execute()
            if result == StrategyResult.successful:
                logger.info(f"Task {task.task_name} with id {task.state.pk} completed")
            elif result == StrategyResult.failed:
                logger.info(
                    f"Task {task.task_name} with id {task.state.pk} failed. Will be retried with delay {task.delay}")
                ExecuteTaskState.apply_async(
                    kwargs={
                        'workflow_instance_id': workflow_instance_id,
                        'task_id': task.pk
                    }, countdown=task.delay)
                return
            elif result in [StrategyResult.permanent_failure, StrategyResult.unknown]:
                logger.info(f"Notify Engineer regarding task state {task.state.pk}")
                return
