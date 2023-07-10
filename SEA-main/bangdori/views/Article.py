from django.shortcuts import render

from bangdori.utils import getModelByName, getCommentModelByName
from profileapp.models import Profile


def article(request, name, pk):
    """
    article : 게시글 내용을 보여주는 view
    """

    context = {}

    # 게시글 정보 불러옴
    article = getModelByName(name)
    need_addr = article().need_addr()
    article = article.objects.all().get(id=pk)
    comment = getCommentModelByName(name)

    try:
        comments = comment.objects.all().filter(article_id=article.id)
    except Exception as e:
        comments = None

    # 조회수 올림
    if request.user.id != article.writer_id or request.user.is_authenticated:
        # 본인 게시글이 아니면 조회수 올림
        article.views += 1

    article.save()

    writer_img = Profile.objects.all().filter(user=article.writer).last()
    if writer_img:
        writer_img = writer_img.image.url

    # Context에 전달
    context['article'] = article
    context['url'] = name
    context['comments'] = comments
    context['writer_img'] = writer_img
    if need_addr:
        context['need_addr'] = need_addr
        context['addr'] = article.addr
        context['lat'] = article.addr.lat
        context['lng'] = article.addr.lng

    return render(request, 'article.html', context)
