from django.utils.deprecation import MiddlewareMixin
from apps.authentication.models import Token
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from apps.sys.views import UserViewSet
from django.http import HttpResponse
from apps.sys.models import User
import json
from rest_framework_jwt.utils import jwt_decode_handler
from jwt import exceptions
from rest_framework.views import APIView


class AuthSerializer(serializers.Serializer):
    details = serializers.CharField(max_length=50)


class AuthenticationMiddleware(MiddlewareMixin):
    """校验用户token有效性"""
    def process_request(self, request):
        if request.path == '/auth/login/':
            return None
        token = request.COOKIES.get('token')
        if token:
            try:
                token = Token.objects.get(token=token)
                token.is_active = True
                token.save()
                return None
            except Token.DoesNotExist as e:
                data = {
                    'details': '用户登录登录信息已失效'
                }
                json_data = json.dumps(data, ensure_ascii=False)
                return HttpResponse(json_data, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)
                # return Response(AuthSerializer(data).data, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)


class TokenToUser(MiddlewareMixin):
    """解析登录用户"""
    # print(request.COOKIES)
    def process_request(self, request):
        try:
            token = request.query_params['token']
        except AttributeError:
            pass
            token = request.COOKIES.get('token')
        if not token:
            return None
        try:
            user_token = jwt_decode_handler(token)
        except exceptions.DecodeError:

            return None
        # 获得user_id
        user_id = user_token["user_id"]
        # 通过user_id查询用户信息
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        request.user = user
        return None

class DataPermissionsMiddleware(MiddlewareMixin):

    """获取用户数据权限"""
    def process_request(self, request):
        user = request.user
        # data_permissions = user.role.data_permissions
        # print(data_permissions)
        return None
