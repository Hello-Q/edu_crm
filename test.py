class UnActiveModelMixin(object):
    """
    删除一个对象，并不真删除，级联将对应外键对象的is_active设置为false，需要外键对象都有is_active字段.
    """
    def perform_destroy(self, instance):
        rel_fileds = [f for f in instance._meta.get_fields() if isinstance(f, ForeignObjectRel)]
        links = [f.get_accessor_name() for f in rel_fileds]

        for link in links:
            manager = getattr(instance, link, None)
            if not manager:
                continue
            if isinstance(manager, models.Model):
                if hasattr(manager, 'is_active') and manager.is_active:
                    manager.is_active = False
                    manager.save()
                    raise ForeignObjectRelDeleteError(u'{} 上有关联数据'.format(link))
            else:
                if not manager.count():
                    continue
                try:
                    manager.model._meta.get_field('is_active')
                    manager.filter(is_active=True).update(is_active=False)
                except FieldDoesNotExist as ex:
                    # 理论上，级联删除的model上面应该也有is_active字段，否则代码逻辑应该有问题
                    logger.warn(ex)
                    raise ModelDontHaveIsActiveFiled(
                            '{}.{} 没有is_active字段, 请检查程序逻辑'.format(
                                manager.model.__module__,
                                manager.model.__class__.__name__
                    ))
        instance.is_active = False
        instance.save()



class DeleteForeignObjectRelModelMixin(object):
    '''删除一个对象，如果他已有外键关联则抛出异常'''
    @POST_OR_GET('force_delete', type='bool', default=False)
    def destroy(self, request, force_delete, *args, **kwargs):
        instance = self.get_object()
        if not force_delete:
            rel_fileds = [f for f in instance._meta.get_fields() if isinstance(f, ForeignObjectRel)]
            links = [f.get_accessor_name() for f in rel_fileds]
            for link in links:
                manager = getattr(instance, link, None)
                if not manager:
                    continue
                # one to one
                if isinstance(manager, models.Model):
                    if hasattr(manager, 'is_active') and manager.is_active:
                        raise ForeignObjectRelDeleteError(u'{} 上有关联数据'.format(link))
                else:
                    try:
                        manager.model._meta.get_field('is_active')
                        if manager.filter(is_active=True).count():
                            raise ForeignObjectRelDeleteError(u'{} 上有关联数据'.format(link))
                    except FieldDoesNotExist as ex:
                        if manager.count():
                            raise ForeignObjectRelDeleteError(u'{} 上有关联数据'.format(link))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)