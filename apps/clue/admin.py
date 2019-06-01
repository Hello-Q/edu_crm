# Register your models here.
from django.contrib import admin
from apps.clue import models

# Register your models here.@admin.register(models.Channel)

#
# class ClueTypeAdmin(admin.ModelAdmin):
#     list_display = ['channel_id', 'channel_type_id', 'del_flag']


@admin.register(models.ChannelType)
class ChannelTypeAdmin(admin.ModelAdmin):
    """
    注册渠道类型管理
    """
    list_display = ['channel_type_id', 'cha_type_name', 'del_flag']


@admin.register(models.Channel)
class ChannelAdmin(admin.ModelAdmin):
    """
    注册渠道管理
    """
    list_display = ['channel_id', 'channel_type_id', 'del_flag']

