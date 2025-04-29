from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('binders/', views.BinderList.as_view(), name='binder-index')
]