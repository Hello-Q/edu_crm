from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _
# Register your models here.


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['org_id', 'org_name', 'org_add', 'contacts_man', 'contacts_tel', 'legal_person']

@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'creator', 'operator']

# @admin.register(models.Department)
# class DepartmentAdmin(admin.ModelAdmin):
#     list_display = ['dep_id', 'org_id', 'dep_type', 'superior_id', 'dname', 'dep_tel', 'creator', 'operator', 'create_time', 'update_time', 'del_flag']


@admin.register(models.User)
class UserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
                                       # 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('其他信息'), {'fields': ('age', 'tel', 'department', 'head_pic', 'nickname', 'roles', 'resources')})
    )