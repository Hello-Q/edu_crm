from rest_framework import viewsets, status
from rest_framework.response import Response


class FalseDelModelViewSet(viewsets.ModelViewSet):

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.del_flag = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        # 自动保存创建人和更新人
        serializer.save(operator=self.request.user, creator=self.request.user)

    def perform_update(self, serializer):
        serializer.save(operator=self.request.user)
