from rest_framework import viewsets, status
from rest_framework.response import Response


class FalseDelModelViewSet(viewsets.ModelViewSet):

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # 假删除操作
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
        serializer.save(operator=self.request.user, creator=self.request.user)

    def perform_update(self, serializer):
        serializer.save(operator=self.request.user)
