from django.contrib import admin

# Register your models here.
from django.db import transaction

from workflowops.models import Workflow, WorkflowDSL, Task
import yaml


@admin.register(WorkflowDSL)
class WorkflowDSLAdmin(admin.ModelAdmin):
    ordering = ['-created']
    actions = [
        'parse_dsl_file'
    ]

    @transaction.atomic
    def _parse_dsl_for_worflows(self, workflow_dsl: WorkflowDSL):
        dsl_file_path = str(workflow_dsl.file)
        with open(dsl_file_path) as file:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            dsl_content = yaml.load(file, Loader=yaml.FullLoader)

        for workflow_name in list(dsl_content['workflows'].keys()):
            workflow = Workflow.objects.create(
                version=Workflow.VersionChoices.v1,
                workflow_namespace=workflow_name,
                user=workflow_dsl.user,
                workflow_dsl=workflow_dsl,
                inputs=':'.join(element for element in dsl_content['workflows'][workflow_name]['input'])
            )
            tasks = dsl_content['workflows'][workflow_name]['tasks']
            task_objects = []
            for i, task in enumerate(tasks):
                task_content = tasks[task]
                task_object = Task.objects.create(
                    workflow=workflow,
                    task_name=task,
                    protocol_type=Task.ProtocolChoices.http,  # Right now just keeping http. This has to made generic
                    action_endpoint=task_content['input']['url'],
                    content_type=Task.ContentChoices.json,
                    protocol_method=Task.MethodChoices.http_get if task_content['input']['method'] == 'GET' else Task.MethodChoices.http_post,
                    retry_count=task_content['retry']['count'],
                    delay=task_content['retry']['delay'],
                    level=i,
                    publish=task_content['publish'],
                    action_message_template=task_content['input'].get('body')

                )
                task_objects.append(task_object)
            for task_object in task_objects:
                task_content = tasks[task_object.task_name]
                success_task_names = task_content.get('on-success')
                if success_task_names:
                    task_object.on_success_next_task = ':'.join(element for element in success_task_names)
                    task_object.save()
                failure_task_names = task_content.get('on-failure')
                if failure_task_names:
                    task_object.on_failure_next_task = ':'.join(element for element in failure_task_names)
                    task_object.save()
        # Get the workflow
        # Create workflow object with necessary details
        # Create the tasks

    def parse_dsl_file(self, request, queryset):
        if len(queryset) > 1:
            self.message_user(request, "Try one at a time for this release")
        workflow_dsl_pks = [pk for pk in queryset.values_list('id', flat=True)]
        for workflow_dsl_pk in workflow_dsl_pks:
            workflow_dsl = WorkflowDSL.objects.get(pk=workflow_dsl_pk)
            self._parse_dsl_for_worflows(workflow_dsl)
        message = "Selected DSL's have been parsed"
        self.message_user(request, message)


@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    pass


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass





