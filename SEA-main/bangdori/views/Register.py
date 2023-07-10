from django.contrib import auth
from django.shortcuts import render, redirect

from bangdori.models import CustomerUser


def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == "POST":
        # register로 POST 요청이 들어오면, 새로운 User를 생성하는 절차
        context = {}

        # 정보 저장
        username = request.POST.get('register_username', None)
        password = request.POST.get('register_user_pwd', None)
        password2 = request.POST.get('register_user_repwd', None)
        email_id = request.POST.get('register_user_email_id', None)
        # 이메일 도메인을 선택에 따라 분기
        email_net = request.POST.get('register_user_email', None)
        if email_net == 'direct':
            # 선택 상자의 const가 direct인 경우, 직접 입력된 칸을 받아옴
            email_net = request.POST.get('register_user_direct_email', None)

        year = request.POST.get('register_user_year', None)
        month = request.POST.get('register_user_month', None)
        day = request.POST.get('register_user_day', None)
        phone = request.POST.get('register_user_phone', None)
        nickname = request.POST.get('register_user_nickname', None)

        # 중복 확인
        if CustomerUser.objects.filter(username=username).exists():
            context['error'] = "사용할 수 없는 ID입니다."

        if password != password2:
            # 비밀번호 틀림
            context['error'] = "비밀번호가 다릅니다."
        elif not email_net:
            context['error'] = "이메일 주소를 입력해주세요."
        else:
            # DB에 저장
            user = CustomerUser.objects.create_user(username=username,
                                                    password=password2,
                                                    email=f'{email_id}@{email_net}',
                                                    birthday=f'{year}-{month}-{day}',
                                                    phone=phone,
                                                    nickname=nickname)

            # 로그인 후 메인으로 이동
            auth.login(request, user)
            return redirect('/')

        return render(request, 'register.html', context)
