from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('binders/', views.BinderList.as_view(), name='binder-index'),
    path('binders/create/', views.BinderCreate.as_view(), name='binder-create'),
    path('binders/<int:pk>/', views.binder_detail, name='binder-detail'),
    path('binders/<int:pk>/update', views.BinderUpdate.as_view(), name='binder-update'),
    path('binders/<int:pk>/delete', views.BinderDelete.as_view(), name='binder-delete'),
    path('accounts/signup/', views.signup, name='signup'),
    path('binders/<int:binder_id>/search/', views.search_cards, name='search-cards'),
    path('binders/<int:binder_id>/cards/<str:card_id>/', views.card_detail_view, name='card-detail'),
    path('binders/<int:binder_id>/add_card/<str:card_id>/', views.add_card_to_binder, name='add_card_to_binder'),
    path('usercard/<int:pk>/', views.user_card_detail, name='user-card-detail'),
    path('usercard/<int:pk>/update', views.UserCardUpdate.as_view(), name='user-card-update'),
    path('usercard/<int:pk>/delete', views.UserCardDelete.as_view(), name='user-card-delete')
]