from django.utils.deprecation import MiddlewareMixin
from apps.authentication.models import Token
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from apps.sys.views import UserViewSet
from django.http import HttpResponse
import json
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
