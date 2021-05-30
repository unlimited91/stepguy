# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from utils.models import BaseUUIDModel
from djchoices import ChoiceItem, DjangoChoices

# Create Workflow
# Upload YAML file
# Verify the file
# Accept the Workflow
# Create the list of tasks
from workflowops.models import Workflow, Task


class WorkflowInstance(BaseUUIDModel):

    workflow = models.ForeignKey(Workflow, on_delete=models.PROTECT)
    # Both the users in the tables (Workflow, Workflow instance) should be the same
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    inputs = models.TextField()

    context = models.TextField()

    class Status(DjangoChoices):
        pending = ChoiceItem('PENDING', 'PENDING')
        in_progress = ChoiceItem('IN-PROGRESS', 'IN-PROGRESS')
        completed = ChoiceItem('COMPLETED', 'COMPLETED')

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.pending)

    class Meta:
        verbose_name = 'WorkflowInstance'
        verbose_name_plural = 'WorkflowInstances'

    def current_task(self):
        pass


class TaskLogs(BaseUUIDModel):

    workflow_instance = models.ForeignKey(WorkflowInstance, on_delete=models.PROTECT)
    task = models.ForeignKey(Task, on_delete=models.PROTECT)
    request_endpoint = models.URLField()
    request_body = models.TextField(null=True, blank=True)
    response_body = models.TextField(null=True, blank=True)

    class Status(DjangoChoices):
        pending = ChoiceItem('PENDING', 'PENDING')
        in_progress = ChoiceItem('IN-PROGRESS', 'IN-PROGRESS')
        successful = ChoiceItem('SUCCESSFUL', 'SUCCESSFUL')
        failed = ChoiceItem('FAILED', 'FAILED')
        permanently_failed = ChoiceItem('PERMANENTLY_FAILED', 'PERMANENTLY_FAILED')
        unknown = ChoiceItem('UNKNOWN', 'UNKNOWN')

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.pending)
    logs = models.TextField()
    # Remove null blank
    no_of_tries = models.IntegerField(null=True, blank=True, default=1)
