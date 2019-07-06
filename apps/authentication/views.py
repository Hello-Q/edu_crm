from django.shortcuts import render
from rest_framework_jwt.views import ObtainJSONWebToken, VerifyJSONWebToken, RefreshJSONWebToken
from apps.sys.models import User
from apps.sys.serializers import UserInfoSerializer
from rest_framework import viewsets, generics
from rest_framework_jwt.utils import jwt_decode_handler
from rest_framework.parsers import MultiPartParser, FileUploadParser
from jwt import exceptions
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from datetime import datetime
from . import models, serializers
# Create your views here.

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER



class LoginView(ObtainJSONWebToken):
    """
    接受用户名和密码进行验证
    验证通过返回token进行登录
    """

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            # 将token存入数据库
            models.Token.objects.create(user=user, token=token, is_active=True)
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(generics.DestroyAPIView):
    queryset = models.Token.objects.all()
    serializer_class = serializers.TokenSerializer

    def destroy(self, request, *args, **kwargs):
        token = request.COOKIES.get('token')
        token = models.Token.objects.get(token=token)
        instance = token
        self.perform_destroy(instance)
        data = {'detail': "注销成功"}
        return Response(data, status=status.HTTP_200_OK)


class TokenVerify(VerifyJSONWebToken):
    """
    对token信息验证如验证成功,返回原token,http状态码200,失败返回错误消息 Error decoding signature.
    """


class TokenRefresh(RefreshJSONWebToken):
    """
    刷新token到期时间,不会返回新的token信息,返回元token信息,但到期时间会刷新
    """


class PersonalInfo(generics.RetrieveUpdateAPIView):
    """
    传入token值,获取用户信息,传入错误token值或者传入token值对应的用户被删除时会返回HTTP404并返回相关错误信息
    """
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = ()
    parser_classes = (MultiPartParser, FileUploadParser,)
    # schema = AutoSchema(manual_fields=[
    #     coreapi.Field(
    #         "token",
    #         required=True,
    #         location="query",
    #         schema=coreschema.String(
    #             title='token',
    #             description="用户token值"
    #         )
    #     ),
    # ])

    def get_user(self, request):

        token = request.query_params.get('token')
        if token is None:
            token = request.COOKIES.get('token')
        # print(request.COOKIES)
        if not token:
            msg = {
                'msg': '未提供token信息'
            }
            # return Response(msg, status=status.HTTP_400_BAD_REQUEST)
            return msg
        # 顶一个空数组来接收token解析后的值
        try:
            user_toke = jwt_decode_handler(token)
        except exceptions.DecodeError as e:
            msg = {
                'msg': 'token值解析异常,请检查token后重试, {}'.format(e)
            }
            return msg
        # 获得user_id
        user_id = user_toke["user_id"]
        # 通过user_id查询用户信息
        try:
            user = self.get_queryset()
            user = user.get(pk=user_id)
        except User.DoesNotExist as e:
            msg = {
                'msg': '未查询到用户,用户可能已被删除, {}'.format(e)
            }
            return msg
        return user

    def retrieve(self, request, *args, **kwargs):
        serializer_context = {
            'request': request,
        }
        user = self.get_user(request)
        if isinstance(user, User):
            user = self.get_user(request)
            roles = user.role.all()
            user.roles = roles
            serializer = UserInfoSerializer(user, context=serializer_context)
            return Response(serializer.data)
        else:
            return Response(user, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_user(request)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
