from django.contrib import admin

# Register your models here.
from userman.models import ApiKey


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    pass
