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


def workflow_file_path(instance, filename):
    """
    Returns a path at runtime for storing the file under year and month wise directory.
    """
    # date = instance.created
    file_type = instance.file_type
    username = instance.user.username
    return f"workflows/{file_type}/{username}/{filename}"


class WorkflowDSL(BaseUUIDModel):

    class FileTypeChoices(DjangoChoices):
        yaml = ChoiceItem('yaml', 'YAML')
        json = ChoiceItem('json', 'JSON')

    file_type = models.CharField(max_length=5, choices=FileTypeChoices.choices)
    file = models.FileField(max_length=255, upload_to=workflow_file_path)
    user = models.ForeignKey(User, on_delete=models.PROTECT)


class Workflow(BaseUUIDModel):

    class VersionChoices(DjangoChoices):
        # v1 is only linear workflows
        v1 = ChoiceItem('v1', 'Version 1')
        v2 = ChoiceItem('v2', 'Version 2')

    version = models.CharField(max_length=5, choices=VersionChoices.choices)
    workflow_namespace = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    # The file that the workflow is mapped to
    workflow_dsl = models.ForeignKey(WorkflowDSL, on_delete=models.PROTECT)

    inputs = models.TextField()

    class Meta:
        verbose_name = 'Workflow'
        verbose_name_plural = 'Workflows'
        unique_together = ['workflow_namespace', 'user']

    def current_task(self):
        pass


class Task(BaseUUIDModel):
    workflow = models.ForeignKey(Workflow, on_delete=models.PROTECT, related_name='tasks')

    class ProtocolChoices(DjangoChoices):
        http = ChoiceItem('http', 'HTTP')
        udp = ChoiceItem('udp', 'UDP')
        display = ChoiceItem('display', 'Display')

    task_name = models.CharField(max_length=100)
    # Whether it's HTTP, UDP et al
    protocol_type = models.CharField(max_length=20, choices=ProtocolChoices.choices)
    # The action to be taken here. Primarily url endpoints if it's networking protocols
    action_endpoint = models.URLField()

    class ContentChoices(DjangoChoices):
        json = ChoiceItem('json', 'JSON')
        xml = ChoiceItem('xml, XML')

    content_type = models.CharField(max_length=10, choices=ContentChoices.choices)

    class MethodChoices(DjangoChoices):
        http_get = ChoiceItem('http_get', 'HTTP_GET')
        http_post = ChoiceItem('http_post', 'HTTP_POST')
        screen_display = ChoiceItem('screen_display', 'Display')
    protocol_method = models.CharField(max_length=10, choices=MethodChoices.choices)

    retry_count = models.IntegerField(null=True, blank=True)
    delay = models.IntegerField(null=True, blank=True)
    level = models.IntegerField(null=True, blank=True)
    on_success_next_task = models.TextField(null=True, blank=True)
    on_failure_next_task = models.TextField(null=True, blank=True)
    publish = models.TextField(null=True, blank=True)
    # In the HTTP world it would be referred to as request body. Couldn't think of a better generic alternative
    action_message_template = models.TextField(null=True, blank=True)
