from django.shortcuts import redirect, render


from bangdori.utils import getCommentModelByName, getModelByName


def commentDelete(request, name, pk, commentId):
    comment = getCommentModelByName(name)
    if request.method == "GET":
        comment.objects.all().get(id=commentId).delete()
        return redirect('article', name=name, pk=pk)
