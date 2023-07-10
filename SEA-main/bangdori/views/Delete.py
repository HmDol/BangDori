from django.shortcuts import redirect, render

from bangdori.utils import getModelByName


def delete(request, name, pk):
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
        article.delete()
        return redirect('board', name=name)
