from django.db import models


class UpvoteHistory(models.Model):
    """
    사용자가 게시물을 추천할 경우, 이에 대한 기록을 저장하는 Model

    Parameters
    ----------
    id : AutoField
        Integer 형식의 Auto Increment를 나타내는 PK
    user : ForeignKey
        추천한 사용자를 나타냄
    board : CharField
        게시판 이름 (예시 : succession)
    article_id : PositiveIntegerField
        게시판의 게시글 id를 나타내고, ForeignKey를 저장하기 위함
    upvote_at : DateTimeField
        추천한 시각을 나타냄
    """

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        'CustomerUser', on_delete=models.CASCADE, verbose_name='user')
    board = models.CharField(max_length=50, verbose_name='board')
    article_id = models.PositiveIntegerField(
        db_column='article_id', null=False)
    upvote_at = models.DateTimeField(db_column='upvote_at', auto_now_add=True)
