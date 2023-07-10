from django.urls import path

from api import views

urlpatterns = [
    # Article 객체 관련 API
    path('article/<str:name>/<int:pk>', views.ArticleInfo.as_view(), name='article_info'),
]
