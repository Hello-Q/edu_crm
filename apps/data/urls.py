
from django.urls import path, include
from . import views

# router.register('base-teacher', views.BaseTeacher)


urlpatterns = [
    path('funnel/', views.FunnelView.as_view()),
    path('conversion/', views.ConversionView.as_view()),
    path('summarized/', views.SummarizedView.as_view()),
]
