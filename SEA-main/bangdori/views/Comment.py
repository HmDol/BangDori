from django.shortcuts import redirect

from bangdori.utils import getModelByName, getCommentModelByName


def comment(request, name, pk):
    user = request.user
    Article = getModelByName(name)
    article = Article.objects.all().get(id=pk)
    comment = getCommentModelByName(name)

    if request.method == "POST":
        comment(article_id=article,
                content=request.POST.get('comment'),
                writer=user).save()

        return redirect('article', name=name, pk=pk)