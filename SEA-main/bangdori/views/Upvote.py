from bangdori.models import UpvoteHistory
from django.http import JsonResponse
from bangdori.utils import getModelByName


def upvote(request):
    user = request.user
    board = request.GET.get('board')
    article_id = request.GET.get('article_id')

    if user is None:
        return JsonResponse({'message': '로그인 해주세요!', 'state': 'NotLogin'}, status=200)

    if request.method == "GET":
        try:
            if (UpvoteHistory.objects.get(
                    user=user, board=board, article_id=article_id)):
                return JsonResponse({'message': '추천 중복', 'state': 'duplicated'}, status=200)
        except UpvoteHistory.DoesNotExist:
            UpvoteHistory.objects.create(
                board=board,
                article_id=article_id,
                user=user).save()
            article = getModelByName(board)
            article = article.objects.all().get(id=article_id)
            article.upvote = article.upvote + 1
            article.save()
        return JsonResponse({'message': '추천 완료', 'state': 'success'}, status=200)
