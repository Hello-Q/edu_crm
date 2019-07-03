from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin
# Register your models here.


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['org_id', 'org_name', 'org_add', 'contacts_man', 'contacts_tel', 'legal_person']


@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['dep_id', 'org_id', 'dep_type', 'superior_id', 'dep_name', 'dep_tel', 'creator', 'operator', 'create_time', 'update_time', 'del_flag']


@admin.register(models.User)
class DepartmentAdmin(UserAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'age', 'last_login',
                    'is_superuser', 'email', 'is_staff']
