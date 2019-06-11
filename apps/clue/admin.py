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

    # def get_model_perms
    # def get_readonly_fields(self, request, obj=None):
    #     print(123, request.user.has_perm('ChannelType.view_ChannelType'))
    #     if not request.user.is_superuser and request.user.has_perm('ChannelType.view_ChannelType'):
    #         return [f.name for f in self.model._meta.fields]
    #     return self.readonly_fields


@admin.register(models.Channel)
class ChannelAdmin(admin.ModelAdmin):
    """
    注册渠道管理
    """
    list_display = ['channel_id', 'channel_type_id', 'del_flag']


@admin.register(models.Clue)
class ClueAdmin(admin.ModelAdmin):
    """
    注册渠道管理
    """
    list_display = ['name']

