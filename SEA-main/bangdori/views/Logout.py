from django.contrib import auth
from django.shortcuts import redirect


def logout(request):
    # del 방식을 이용하지 않고, auth에서 제공하는 메서드를 이용
    auth.logout(request)
    return redirect('/index')
