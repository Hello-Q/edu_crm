from rest_framework import viewsets, status
from rest_framework.response import Response


class FalseDelModelViewSet(viewsets.ModelViewSet):

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # 假删除操作
        if instance.del_flag:
            return Response({"detail": "资源不存在或已被删除"}, status=status.HTTP_404_NOT_FOUND)
        instance.del_flag = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        # 按数据权限过滤数据(未完成)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        # 自动保存创建人和更新人
        user = self.request.user
        organization = user.department.all()[0].organization
        serializer.save(operator=user, creator=user, organization=organization)

    def perform_update(self, serializer):
        serializer.save(operator=self.request.user)
