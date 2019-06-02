from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.Organization)
class ClueTypeAdmin(admin.ModelAdmin):
    list_display = ['org_id', 'org_name', 'org_add', 'contacts_man', 'contacts_tel', 'legal_person']

@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['dep_id', 'org_id', 'dep_type', 'superior_id', 'dep_name', 'dep_tel']
