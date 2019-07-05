from django.db import models

# Create your models here.


class Token(models.Model):
    token_id = models.AutoField(primary_key=True, verbose_name='TOKEN_id')
    token = models.CharField(max_length=1000, verbose_name='token值')
    user = models.ForeignKey('sys.User', on_delete=models.CASCADE, verbose_name='归属用户')
    is_active = models.BooleanField(verbose_name='活跃用户')
