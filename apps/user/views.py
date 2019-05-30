from rest_framework.viewsets import GenericViewSet
from . import serializers
from . import models
from rest_framework import viewsets, generics, mixins
from rest_framework_jwt.views import ObtainJSONWebToken, VerifyJSONWebToken, RefreshJSONWebToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
# Create your views here.
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from django_filters.rest_framework import DjangoFilterBackend

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


# class LoginInfo(mixins.RetrieveModelMixin,
#               mixins.UpdateModelMixin,
#               mixins.DestroyModelMixin,
#               generics.GenericAPIView):
#     queryset = models.UserProfile.objects.all()
#     serializer_class = serializers.UserSerializer
#
#     def get(self, request, *args, **kwargs):
#         print()
#         return self.retrieve(request, *args, **kwargs)
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


from django.http import HttpResponse, JsonResponse
from rest_framework_jwt.utils import jwt_decode_handler
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework import status
from jwt import exceptions
import coreapi
from rest_framework.schemas import AutoSchema, ManualSchema
from rest_framework.compat import coreapi, coreschema


class GetUserInfo(generics.RetrieveAPIView):
    """
    传入token值,获取用户信息,传入错误token值或者传入token值对应的用户被删除时会返回HTTP404并返回相关错误信息
    """
    queryset = models.UserProfile.objects.all()
    serializer_class = models.UserProfile
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            "token",
            required=True,
            location="query",
            schema=coreschema.String(
                title='token',
                description="用户token值"
            )
        ),
    ])

    def retrieve(self, request, *args, **kwargs):
        user = self.get_queryset()
        # 获取请求参数token的值
        token = request.GET.get('token')
        if not token:
            return Response({'msg': '未提供token信息'}, status=status.HTTP_400_BAD_REQUEST)
        # 顶一个空数组来接收token解析后的值
        try:
            toke_user = jwt_decode_handler(token)
        except exceptions.DecodeError as e:
            return Response({'msg': 'token值解析异常,请检查token后重试, {}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)
        # return Response({'msg': '未查询到用户,用户可能已被删除'}, status=status.HTTP_404_NOT_FOUND)
        # 获得user_id
        user_id = toke_user["user_id"]
        # 通过user_id查询用户信息
        try:
            user_info = user.get(pk=user_id)
        except models.UserProfile.DoesNotExist as e:
            return Response({'msg': '未查询到用户,用户可能已被删除, {}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.UserSerializer(user_info)
        return Response(serializer.data)




