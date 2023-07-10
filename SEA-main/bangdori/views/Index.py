from django.shortcuts import redirect, render

from bangdori.models import BoardArticle, DabangArticle, SuccessionArticle, GroupArticle, EssentialsArticle
from bangdori.utils import getAllArticles, getCommentModelByName, addCommentsToTitle
from project.settings import INDEX_ARTICLES


def goIndex(request):
    return redirect('index')


def index(request):
    context = {}
    # 게시글 정보를 저장할 dict
    articles = {}
    # 게시글 데이터 가져옴
    data = getAllArticles()

    # 자를 갯수
    cut = INDEX_ARTICLES

    # 게시글이 없는 경우에 예외처리를 하지 않으면 오류가 날 수 있음
    if len(data) > 0:
        # 핫 게시물은 upvote 순으로 정렬
        # addCommentsToTitle로 댓글 수도 추가
        articles['best'] = addCommentsToTitle(sorted(data, key=lambda x: x['upvote'], reverse=True)[:cut])

        # 최신 게시물은 date 순으로 정렬
        articles['new'] = addCommentsToTitle(sorted(data, key=lambda x: x['date'], reverse=True)[:cut])

        # 각 게시판별 글
        articles['board'] = addCommentsToTitle(
            [x.to_dict() for x in BoardArticle.objects.all().order_by('-date')][:cut])
        articles['dabang'] = addCommentsToTitle(
            [x.to_dict() for x in DabangArticle.objects.all().order_by('-date')][:cut])
        articles['succession'] = addCommentsToTitle(
            [x.to_dict() for x in SuccessionArticle.objects.all().order_by('-date')][:cut])
        articles['group'] = addCommentsToTitle(
            [x.to_dict() for x in GroupArticle.objects.all().order_by('-date')][:cut])
        articles['essentials'] = addCommentsToTitle(
            [x.to_dict() for x in EssentialsArticle.objects.all().order_by('-date')][:cut])

        context['articles'] = articles
    return render(request, 'index.html', context)
