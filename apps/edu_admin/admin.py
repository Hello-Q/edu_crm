from django.contrib import admin

# Register your models here.
from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.Course)
class ClueTypeAdmin(admin.ModelAdmin):
    exclude = []


@admin.register(models.Subjects)
class SubjectsAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['tea_id', 'user_id']
