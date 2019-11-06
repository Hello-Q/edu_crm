from rest_framework import viewsets, status
from rest_framework.response import Response
from .permissions import DataPermission
from rest_framework.generics import DestroyAPIView


class FalseDestroyAPIView(DestroyAPIView):
    """
    用户执行删除操作时，设置数据库del_flag=Ture，执行假删除操作
    """
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # 假删除操作
        if instance.del_flag:
            return Response({"detail": "资源不存在或已被删除"}, status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.del_flag = True
        instance.save()



class FalseDelModelViewSet(viewsets.ModelViewSet):
    data_permission_class = DataPermission

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # 假删除操作
        if instance.del_flag:
            return Response({"detail": "资源不存在或已被删除"}, status=status.HTTP_404_NOT_FOUND)
        instance.del_flag = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        # 过滤删除以及不符合数据权限数据
        queryset = self.filter_queryset(self.get_queryset()).filter(del_flag=False)
        if not request.user.is_superuser:
            data_permission = self.data_permission_class()
            queryset = data_permission.get_perm_queryset(queryset.model, request, queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        # 自动保存创建人和更新人
        user = self.request.user
        organization = user.department.all()[0].organization
        serializer.save(operator=user, creator=user, organization=organization)

    def perform_update(self, serializer):
        serializer.save(operator=self.request.user)
