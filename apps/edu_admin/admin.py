from django.contrib import admin

# Register your models here.
from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.Course)
class ClueTypeAdmin(admin.ModelAdmin):
    list_display = ['cou_id']
