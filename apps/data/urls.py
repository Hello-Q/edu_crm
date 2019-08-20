
from django.urls import path, include
from . import views

# router.register('base-teacher', views.BaseTeacher)


urlpatterns = [
    path('funnel/', views.FunnelView.as_view()),
    path('test/', views.ConversionView.as_view()),
]
