from rest_framework.viewsets import GenericViewSet
from . import serializers
from . import models
from rest_framework import viewsets, generics
from rest_framework_jwt.views import ObtainJSONWebToken, VerifyJSONWebToken, RefreshJSONWebToken
from rest_framework.views import APIView
from rest_framework import mixins
# Create your views here.
from rest_framework_jwt.serializers import JSONWebTokenSerializer


class Login(ObtainJSONWebToken):
    """
    接受用户名和密码进行验证
    验证通过返回token进行登录
    """


class TokenVerify(VerifyJSONWebToken):
    """
    对token信息验证如验证成功,返回原token,http状态码200,失败返回错误消息 Error decoding signature.
    """


class TokenRefresh(RefreshJSONWebToken):
    """
    刷新token到期时间,不会返回新的token信息,返回元token信息,但到期时间会刷新
    """


class User(viewsets.ModelViewSet):
    """
    对系统用户进行数据操作
    """
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserSerializer


