from django.shortcuts import render
from django.views import View

from bangdori.utils import getModelByName, getCommentModelByName


class SearchAll(View):
    """
    SearchAll : header에 위치하는 검색 기능을 사용하기 위한 클래스
    """

    def post(self, request):
        # 페이지에 넘겨줄 Context
        context = {}
        context['is_search'] = True
        context['is_global_search'] = True

        # 모든 게시판 객체 가져옴
        boards = getModelByName(None, True)
        # 검색어 가져옴
        keyword = request.POST.get('search_keyword')

        # 게시물 검색해오는 부분
        result = list()
        for board in boards:
            # 모든 게시판에서 키워드를 포함한 글을 가져옴
            articles = board.objects.all().filter(title__contains=keyword)
            # 검색 결과가 없는 것은 제외
            if articles.count() > 0:
                for article in articles:
                    # dict로 변환하여 저장
                    result.append(article.to_dict())

        # 날짜순으로 정렬
        result = sorted(result, key=lambda x: x['date'], reverse=True)
        context['articles'] = result
        context['keyword'] = keyword

        # 댓글 가져옴
        context['comments'] = {x['id']: getCommentModelByName(x['url']).objects.all().filter(
            article_id=x['id']).count() for x in context['articles']}


        # Pagination은 구현되어 있지 않음
        return render(request, 'board.html', context)


class SearchArticle(View):
    """
    SearchArticle : 게시판 내에서 검색을 위한 클래스
    """

    def post(self, request, name):
        # 페이지에 넘겨줄 Context
        context = {}
        context['is_search'] = True
        options = request.POST.get('search-type')

        # 모든 게시판 객체 가져옴
        board = getModelByName(name)
        # 검색어 가져옴
        keyword = request.POST.get('board-search-keyword')

        # 게시물 검색해오는 부분
        result = board.objects.all()

        # 조건에 맞도록 검색하는 부분
        if options == 'search-tc':
            x = result.filter(title__contains=keyword)
            x |= result.filter(content__contains=keyword)
            result = x
        elif options == 'search-t':
            result = result.filter(title__contains=keyword)
        elif options == 'search-c':
            result = result.filter(content__contains=keyword)
        elif options == 'search-w':
            result = result.filter(writer__username=keyword)
        elif options == 'search-cmt':
            pass

        # 날짜 순으로 정렬
        result = result.order_by('-date')

        context['articles'] = result
        # 게시판 내 검색이므로, 주소를 지정해주어야 함
        context['url'] = name

        # 댓글 가져옴
        comments = getCommentModelByName(name)
        context['comments'] = {x.id: comments.objects.all().filter(
            article_id=x).count() for x in context['articles']}

        # Pagination은 구현되어 있지 않음
        return render(request, 'board.html', context)
