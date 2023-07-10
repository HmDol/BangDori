from django.http import JsonResponse

from bangdori.models import CustomerUser


def id_check(request):
    # 아이디나 닉네임이 존재하는지 확인, 둘 중 하나를 가져옴
    username = request.GET.get('user', None)
    nickname = request.GET.get('nickname', None)

    try:
        user = None

        # 경우에 따른 유효성 검사
        if username:
            user = CustomerUser.objects.all().filter(username=username).last()
        elif nickname:
            user = CustomerUser.objects.all().filter(nickname=nickname).last()
    except Exception as e:
        user = None
    result = {
        'result': 'success',
        'data': "not exist" if user is None else "exist"
    }

    return JsonResponse(result)
