from django.contrib import admin
from apps.personnel import models
# Register your models here.


@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['dep_id', 'org_id', 'dep_type', 'superior_id', 'dep_name', 'dep_tel']
