from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('binders/', views.BinderList.as_view(), name='binder-index'),
    path('binders/create/', views.BinderCreate.as_view(), name='binder-create'),
    path('binders/<int:pk>/', views.BinderDetail.as_view(), name='binder-detail'),
    path('accounts/signup/', views.signup, name='signup'),

]