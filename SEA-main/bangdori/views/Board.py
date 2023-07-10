from django.core.paginator import Paginator
from django.shortcuts import render

from bangdori.utils import getModelByName, getArticlesByAddress, getCommentModelByName
from project.settings import MAX_ARTICLES


def board(request, name):
    """
    board : 게시판 목록을 보여주는 view
    """

    # 페이지에 넘겨줄 Context
    context = {}

    # 게시판 내용 불러올 Article 객체
    articles = getModelByName(name)
    need_sorted_addr = articles().need_sorted_addr()

    # 페이지 정보 전달
    # context['name'] : 페이지가 표시되는 한글 이름
    context['name'] = articles._meta.verbose_name
    # context['url'] : 페이지에서 url로 전달받은 이름
    context['url'] = name

    # 모든 글 가져옴, 날짜 내림차순으로 조회
    articles = articles.objects.all().order_by('-date')

    # 주소 순으로 정렬이 필요한 경우
    if need_sorted_addr:
        articles = getArticlesByAddress(request.user, articles)

    # Paginator 사용
    paginator = Paginator(articles, MAX_ARTICLES)
    # GET 요청이 들어오면 page 파라미터를 읽어옴
    page = int(request.GET.get('page', 1))

    # 현재 페이지에 맞는 게시물 목록을 Context로 넘겨줌
    context['articles'] = paginator.get_page(page)

    # 댓글 가져옴
    comments = getCommentModelByName(name)
    context['comments'] = {x.id: comments.objects.all().filter(
        article_id=x).count() for x in context['articles']}
    return render(request, 'board.html', context)
