from django.urls import path

from . import views
from .views import ProfileCreateView, ProfileUpdateView

app_name = 'profileapp'

urlpatterns = [
    path('create/', ProfileCreateView.as_view(), name='create'),
    path('view', views.view, name='view'),
    path('update/<int:pk>', ProfileUpdateView.as_view(), name='update'),
    path('mypage/', views.mypage),
    path('myinfo/', views.myinfo, name='myinfo'),
    path('mypost/', views.mypost, name='mypost'),
    path('favorites/', views.favorites, name='favorites'),
    path('address/', views.Address.as_view(), name='address'),
    path('corporate/', views.corporate, name='corporate'),
    path('create/small/<int:pk>', views.AccountUpdateView.as_view(), name='small'),
]
