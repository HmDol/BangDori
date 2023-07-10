import requests
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect, render
from django.views import View

from bangdori.models import CustomerUser


def login(request):
    # 기본이 POST로 수정
    context = {}
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    if request.method == "POST":
        # AuthenticationForm으로부터 인증 Form을 받아옴
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            # cleaned_data 형식으로 아이디와 비밀번호를 가져옴
            # Django의 auth 클래스를 사용해 로그인
            user = auth.authenticate(
                request=request, username=username, password=password)
            # 해당하는 유저가 존재해서 로그인이 가능한 경우
            if user is not None:
                auth.login(request, user)
                return redirect('/index')
        else:
            if not (username and password):
                context['error'] = "빈칸없이 입력해주세요."
            else:
                if CustomerUser.objects.filter(username=username):
                    user = CustomerUser.objects.get(username=username)
                    if not check_password(password, user.password):
                        request.session['user'] = user.username
                        context['error'] = "해당 회원정보가 존재하지 않습니다."
                        return render(request, 'login.html', context)
    else:
        return render(request, 'login.html', context)

    return render(request, 'login.html', context)


class kakaologin(View):
    def get(self, request):
        kakao_api = "https://kauth.kakao.com/oauth/authorize?response_type=code"
        redirect_uri = "http://localhost:8000/login/kakao/callback/"
        client_id = "061401748822539ecf6d032fcc459c14"

        return redirect(
            f"{kakao_api}&client_id={client_id}&redirect_uri={redirect_uri}")


class kakaocallback(View):
    def get(self, request):
        data = {
            "grant_type": "authorization_code",
            "client_id": "061401748822539ecf6d032fcc459c14",
            "redirection_uri": "http://localhost:8000/login/kakao",
            "code": request.GET["code"]
        }
        kakao_token_api = "https://kauth.kakao.com/oauth/token"
        access_token = requests.post(kakao_token_api, data=data).json()[
            "access_token"]

        kakao_user_api = "https://kapi.kakao.com/v2/user/me"
        header = {"Authorization": f"Bearer ${access_token}"}
        json = requests.get(kakao_user_api, headers=header).json()
        try:
            user = CustomerUser.objects.all().get(provider=json['id'])
        except CustomerUser.DoesNotExist:
            user = None
        if user is not None:
            auth.login(request, user)
            return redirect('/index')
        user = CustomerUser.objects.create_user(provider=json['id'],
                                                email=json['kakao_account']['email'],
                                                username='kakao_' +
                                                         json['kakao_account']['profile']['nickname'],
                                                nickname='kakao_' +
                                                         json['kakao_account']['profile']['nickname']
                                                )
        user.save()
        auth.login(request, user)
        return redirect('/index')


class googlelogin(View):
    def get(self, request):
        google_api = "https://accounts.google.com/o/oauth2/v2/auth?response_type=code"
        redirect_uri = "http://localhost:8000/login/google/callback/"
        client_id = "423096054112-5hoh9i9p6i9bppac2cs3dea30cc5jvr6.apps.googleusercontent.com"
        scope = "https://www.googleapis.com/auth/userinfo.email " + \
                "https://www.googleapis.com/auth/userinfo.profile"

        return redirect(
            f"{google_api}&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}")


class googlecallback(View):
    def get(self, request):
        google_token_api = 'https://oauth2.googleapis.com/token'
        # secret key 일부러 빼놓음.
        data = {
            "code": request.GET['code'],
            "client_id": "423096054112-5hoh9i9p6i9bppac2cs3dea30cc5jvr6.apps.googleusercontent.com",
            "redirect_uri": "http://localhost:8000/login/google/callback/",
            "client_secret": "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",
            "grant_type": "authorization_code",
        }
        access_token = requests.post(google_token_api, data=data).json()[
            "access_token"]
        google_user_api = "https://www.googleapis.com/oauth2/v3/userinfo"
        json = requests.get(google_user_api,
                            params={"access_token": access_token}).json()
        # 받아오는 숫자가 16자리로 너무 커서 SQL에서 변환 도중 오류가 남

        try:
            user = CustomerUser.objects.all().get(provider=json['sub'])
        except CustomerUser.DoesNotExist:
            user = None
        if user is not None:
            auth.login(request, user)
            return redirect('/index')

        user = CustomerUser.objects.create_user(provider=json['sub'],
                                                email=json['email'],
                                                username='google_' +
                                                         json['name'],
                                                nickname='google_' +
                                                         json['name'],
                                                )
        auth.login(request, user)
        return redirect('/index')


class naverlogin(View):
    def get(self, request):
        naver_api = "https://nid.naver.com/oauth2.0/authorize?response_type=code"
        redirect_uri = "http://localhost:8000/login/naver/callback/"
        client_id = "wbvRsxRzlRkolqqiMZq1"
        state = "bangdori"
        return redirect(
            f"{naver_api}&client_id={client_id}&redirect_uri={redirect_uri}&state={state}")


class navercallback(View):
    def get(self, request):
        naver_token_api = "https://nid.naver.com/oauth2.0/token"
        data = {
            "code": request.GET['code'],
            "client_id": "wbvRsxRzlRkolqqiMZq1",
            "redirect_uri": "http://localhost:8000/login/naver/callback/",
            "client_secret": "ff_Bbw3Iba",
            "state": "bandori",
            "grant_type": "authorization_code",
        }
        access_token = requests.post(naver_token_api, data=data).json()[
            'access_token']
        naver_user_api = "https://openapi.naver.com/v1/nid/me"
        header = {"Authorization": f"Bearer ${access_token}"}

        json = requests.get(naver_user_api,
                            params={"access_token": access_token}).json()['response']
        uid = int(json['mobile_e164'][1:])
        try:
            user = CustomerUser.objects.all().get(provider=uid)
        except CustomerUser.DoesNotExist:
            user = None
        if user is not None:
            auth.login(request, user)
            return redirect('/index')
        user = CustomerUser.objects.create_user(provider=uid,
                                                email=json['email'],
                                                birthday=json['birthyear'] +
                                                         '-' + json['birthday'],
                                                username='naver_' +
                                                         json['nickname'],
                                                nickname='naver_' +
                                                         json['nickname'],
                                                phone=json['mobile'],
                                                )
        auth.login(request, user)
        return redirect('/index')
