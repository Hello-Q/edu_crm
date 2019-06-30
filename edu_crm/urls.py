"""edu_crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls
from django.conf import settings
from django.conf.urls.static import static


def prod_static_url():
    """
    prod 模式下的 url 适配
    """
    from django.views import static
    urlpattern = path(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT }, name='static')
    return urlpattern


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),  # 登录入口
    path('docs/', include_docs_urls(title='API文档',
                                    description='-教育版',
                                    )),
    prod_static_url(),
    path('sys-set/', include('apps.sys_set.urls')),
    path('clue/', include('apps.clue.urls')),
    path('edu_admin/', include('apps.edu_admin.urls'))

] \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
