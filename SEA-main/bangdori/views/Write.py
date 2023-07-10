from django.shortcuts import redirect, render

import bangdori
from bangdori.models import CustomerUser
from bangdori.utils import getModelByName


def write(request, name):
    """
    write : 게시글을 작성하는 view
    """
    context = {}

    # 현재 로그인된 사용자의 정보를 가져옴
    user: CustomerUser = request.user

    # 현재 게시판에 맞는 모델을 가져옴
    article = getModelByName(name)
    need_addr = article().need_addr()
    need_sorted_addr = article().need_sorted_addr()

    # 페이지 정보 전달
    # context['name'] : 페이지가 표시되는 한글 이름
    context['name'] = article._meta.verbose_name
    # context['need_addr'] : 주소 등록이 필요한지에 대한 여부
    context['need_addr'] = need_addr

    if request.method == "POST":
        # 이미지 받아옴

        # 게시글 작성
        article = article(title=request.POST.get('title'),
                          writer=CustomerUser.objects.get(username=user),
                          content=request.POST.get('content'),
                          attr=request.POST.get('alignStatus'))

        # 사진 업로드
        try:
            _, img = request.FILES.popitem()
            img = img[0]
            article.img = img
        except:
            pass

        # 주소가 필요한 경우, article의 FK 필드인 addr에 새로운 주소를 만들어 저장
        if need_addr:
            article.addr = bangdori.models.Address().createFromPost(request)

        # 글에 주소 등록은 필요 없는데, 이를 사용자의 주소로 가져와야 할 경우
        if not need_addr and need_sorted_addr:
            # need_addr은 주소 등록이 필요 없으므로 False이고,
            # need_sorted_addr은 주소 순으로 정렬해야 할 경우 True이면,
            # 주소 등록은 없지만 주소 순으로 정렬해야 한다는 의미가 되므로,
            # 이러한 경우 사용자의 주소를 가져와 해당 글의 주소로 등록한다.
            article.addr = user.addr

        # 게시글 저장
        article.save()

        # 게시판으로 다시 돌아감
        return redirect('board', name=name)

    return render(request, 'write.html', context)
