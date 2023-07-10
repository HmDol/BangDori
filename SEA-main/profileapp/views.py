from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView

import bangdori
from bangdori.models import CustomerUser, UpvoteHistory
from bangdori.utils import getModelByName
from .forms import ProfileCreateForm, AccountUpdateForm
from .models import *


# Create your views here.
class ProfileCreateView1(CreateView):
    model = Profile
    context_object_name = 'target_profile'
    form_class = ProfileCreateForm
    success_url = reverse_lazy('index')
    template_name = 'create.html'

    def form_valid(self, form):  # ProfileCreationForm의 data가 2번째 파라미터에 들어 있어요.
        # 임시로 저장함.<commit=False> 키워드 인자를 이용해서
        temp_profile = form.save(commit=False)
        temp_profile.user = self.request.user

        temp_profile.save()  # self는 view에서 가져온 self임. 또, 웹브라우저에서 입력 받은 값이 우항 좌항이 db에서 가져온값
        return super().form_valid(form)


class ProfileCreateView(View):
    def get(self, request):
        context = {}

        return render(request, 'create.html', context)

    def post(self, request):
        context = {}
        # 사진 업로드
        img = None
        try:
            _, img = request.FILES.popitem()
            img = img[0]
        except:
            pass

        if img:
            profile = Profile.objects.all().filter(user=request.user).last()
            if profile is None:
                profile = Profile(user=request.user)

            profile.image = img
            profile.save()

        request.user.nickname = request.POST.get('nicknameBox')
        request.user.save()

        return redirect('index')


class ProfileUpdateView(UpdateView):
    model = Profile
    context_object_name = 'target_profile'
    form_class = ProfileCreateForm
    success_url = reverse_lazy('index')
    template_name = 'update.html'

    def update(request, user_id):
        user = get_object_or_404(CustomerUser, pk=user_id)
        user.nickname = request.GET['nickname']
        user.save()
        return redirect('/index')


def view(request):
    return render(request, 'view.html')


def profile(request):
    return render(request, 'profile.html')


def mypage(request):
    return redirect('profileapp:myinfo')


def myinfo(request):
    """
    내 정보
    """
    context = {}
    user: CustomerUser = request.user
    context['email'] = user.email
    context['phone'] = user.phone

    if request.method == 'POST':
        user.set_password(request.POST.get('password'))
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')

        user.save()

        return redirect('index')

    return render(request, 'myinfo.html', context)


def mypost(request):
    """
    내가 쓴 글
    """
    context = {}

    # 모든 게시판 객체 가져옴
    boards = getModelByName(None, True)

    # 게시물 검색해오는 부분
    result = list()
    for board in boards:
        # 모든 게시판에서 작성자가 현재 작성자인 글을 찾아옴
        articles = board.objects.all().filter(writer=request.user)
        # 검색 결과가 없는 것은 제외
        if articles.count() > 0:
            for article in articles:
                # dict로 변환하여 저장
                result.append(article.to_dict())

    # 날짜순으로 정렬
    result = sorted(result, key=lambda x: x['date'], reverse=True)
    context['articles'] = result

    return render(request, 'mypost.html', context)


def favorites(request):
    """
    즐겨찾기
    """
    context = {}

    # 내가 추천한 게시글 가져옴
    history = UpvoteHistory.objects.all().filter(user_id=request.user)

    # 모든 게시판 객체 가져옴
    boards = getModelByName(None, True)

    # 게시물 검색해오는 부분
    result = list()

    for h in history:
        # 추천한 게시판 객체 가져옴
        board = getModelByName(h.board)
        # 결과에 추가
        result.append(board.objects.all().filter(id=h.article_id).last().to_dict())

    # 날짜순으로 정렬
    result = sorted(result, key=lambda x: x['date'], reverse=True)
    context['articles'] = result
    return render(request, 'favorites.html', context)


def small(request):
    """
    닉네임 변경 작은 창
    """
    return render(request, 'small.html')


def corporate(request):
    """
    사업자 등록
    """
    context = {}

    corp = request.user.corp_num
    if not corp:
        corp = ""
    context['corp'] = corp

    if request.method == 'POST':
        request.user.corp_num = request.POST.get('corp')
        request.user.save()

        return redirect('profileapp:corporate')

    return render(request, 'corporate-registration.html', context)


class Address(View):
    def get(self, request):
        if request.user.is_anonymous:
            # 로그인되지 않은 상태
            return redirect(reverse('index'))

        context = {}
        context['addr'] = request.user.addr

        # 주소 등록 페이지
        return render(request, 'address.html', context)

    def post(self, request):
        # 주소 모델 생성
        addr = bangdori.models.Address().createFromPost(request)

        # 사용자 모델 가져옴
        user: CustomerUser = request.user
        # 이미 등록되어 있으면 해당 데이터를 삭제하고 저장
        if user.addr:
            user.addr.delete()

        # 저장
        user.addr = addr
        user.save()

        context = {}
        context['addr'] = request.user.addr

        # 주소 등록 페이지
        return render(request, 'address.html', context)


class AccountUpdateView(UpdateView):
    model = CustomerUser
    form_class = AccountUpdateForm
    context_object_name = 'target_user'
    success_url = reverse_lazy('index')
    template_name = 'small.html'
