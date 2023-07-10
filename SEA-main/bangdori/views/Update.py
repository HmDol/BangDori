from django.shortcuts import redirect, render

from bangdori.utils import getModelByName


def update(request, name, pk):
    """
    update : 게시글 update하는 view
    """
    user = request.user
    Article = getModelByName(name)
    article = Article.objects.all().get(id=pk)

    if article.writer != user:
        return redirect('article', name=name, pk=pk)

    if request.method == "POST":
        # 게시글 수정
        article.title = request.POST.get('title')
        article.content = request.POST.get('content')
        article.attr = request.POST.get('alignStatus')

        try:
            _, img = request.FILES.popitem()
            img = img[0]
            article.img = img
        except:
            pass

        article.save()
        return redirect('article', name=name, pk=pk)

    context = {}
    context['title'] = article.title
    context['content'] = article.content
    context['isEdit'] = True
    context['attr'] = article.attr

    try:
        context['img'] = article.img.url
    except:
        pass

    return render(request, 'write.html', context)
