from django.contrib import admin

# Register your models here.
from workflowapi.models import WorkflowInstance, TaskLogs


@admin.register(WorkflowInstance)
class WorkflowInstanceAdmin(admin.ModelAdmin):
    pass


@admin.register(TaskLogs)
class TaskLogsAdmin(admin.ModelAdmin):
    pass
