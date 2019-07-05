# Create your views here.
from django.contrib.auth.models import Permission, Group
from jwt import exceptions
from rest_framework import status
from rest_framework import viewsets, generics
from rest_framework.compat import coreapi, coreschema
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from rest_framework_jwt.utils import jwt_decode_handler
from rest_framework_jwt.views import ObtainJSONWebToken, VerifyJSONWebToken, RefreshJSONWebToken
from django.core.files.base import ContentFile
from rest_framework.parsers import MultiPartParser, FileUploadParser
from apps.sys import models
from apps.sys import serializers


class LoginView(ObtainJSONWebToken):
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


class PersonalInfo(generics.RetrieveUpdateAPIView):
    """
    传入token值,获取用户信息,传入错误token值或者传入token值对应的用户被删除时会返回HTTP404并返回相关错误信息
    """
    queryset = models.User.objects.all()
    serializer_class = serializers.UserInfoSerializer
    permission_classes = ()
    parser_classes = (MultiPartParser, FileUploadParser,)
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
        except models.User.DoesNotExist as e:
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
        if isinstance(user, models.User):
            user = self.get_user(request)
            roles = user.role.all()
            user.roles = roles
            serializer = serializers.UserInfoSerializer(user, context=serializer_context)
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


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    操作公司数据
    """
    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    部门数据
    """
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    对系统用户进行数据操作
    """
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class PermissionViewSet(viewsets.ModelViewSet):
    """
    权限列表
    """
    queryset = Permission.objects.all()
    serializer_class = serializers.PermissionSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    用户组
    """
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer


class RoleViewSet(viewsets.ModelViewSet):
    """
    角色
    """
    queryset = models.Role.objects.all()
    serializer_class = serializers.RoleSerializer


class ResourceViewSet(viewsets.ModelViewSet):
    """资源"""
    queryset = models.Resource.objects.all()
    serializer_class = serializers.ResourceSerializer
