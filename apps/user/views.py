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


class GetUserInfo(APIView):


    def get(self, request):
        User = get_user_model()
        if request.method == 'GET':
            print(1344)
            # 获取请求参数token的值
            token = request.GET.get('token')
            print(1213, token)
            # 顶一个空数组来接收token解析后的值
            toke_user = []
            toke_user = jwt_decode_handler(token)
            # 获得user_id
            user_id = toke_user["user_id"]
            # 通过user_id查询用户信息
            user_info = User.objects.get(pk=user_id)
            serializer = serializers.UserSerializer(user_info)

            return Response(serializer.data)




