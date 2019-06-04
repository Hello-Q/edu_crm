from django.apps import AppConfig
import os

default_app_config = 'apps.edu_admin.EduAdminConfig'


# 获取当前App名称
def get_current_app_name(_file):
    _dir = os.path.split(os.path.dirname(os.path.dirname(_file)))[-1]
    superior_dir = os.path.split(os.path.dirname(os.path.abspath(_file)))[-1]
    return _dir + '.' + superior_dir


class EduAdminConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = '教务管理'
