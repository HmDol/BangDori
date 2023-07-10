from django.urls import path
from . import views

NAME = 'APP'
urlpatterns = [
    path('', views.goIndex, name='go'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('idcheck/', views.id_check, name='idcheck'),
    path('detail/<int:pk>', views.DetailView.as_view(), name='detail'),
    # path('accountupdate/<int:pk>', views.AccountUpdateView.as_view(), name='update'),
    path('board/<str:name>/', views.board, name='board'),
    path('board/<str:name>/search/',
         views.SearchArticle.as_view(), name='searcharticle'),
    path('board/<str:name>/<int:pk>', views.article, name='article'),
    path('board/<str:name>/write/', views.write, name='write'),
    path('board/<str:name>/update/<int:pk>', views.update, name='update'),
    path('board/<str:name>/delete/<int:pk>', views.delete, name='delete'),
    path('board/<str:name>/<int:pk>/comment', views.comment, name='comment'),
    path('board/<str:name>/<int:pk>/comment/<int:commentId>',
         views.commentDelete, name='commentDelete'),
    path('board/upvote', views.upvote, name='upvote'),
    path('findID/', views.findID, name='findID'),
    path('findID/sms', views.SMS),
    path('sms/send', views.SmsSendView.as_view()),

    path('sms/auth', views.SmsVerifyView.as_view()),
    path('findPW1/', views.findPW1, name='findPW1'),
    path('findPW1/findPW2/', views.findPW2, name='findPW2'),
    path('login/kakao', views.kakaologin.as_view(), name='kakaoLogin'),
    path('login/kakao/callback/',
         views.kakaocallback.as_view(), name='kakaoCallback'),
    path('login/google', views.googlelogin.as_view(), name='googleLogin'),
    path('login/google/callback/',
         views.googlecallback.as_view(), name='googleCallback'),
    path('login/naver', views.naverlogin.as_view(), name='naverLogin'),
    path('login/naver/callback/',
         views.navercallback.as_view(), name='naverCallback'),
    path('findPW1/findPW2/smspw', views.SMSPW, name='smspw'),
    path('search/', views.SearchAll.as_view(), name='searchall'),

    path('findID/sms/ShowID', views.showID, name='showID'),
    path('findPW1/findPW2/smspw/showPW/', views.showPW, name='showPW')
]
