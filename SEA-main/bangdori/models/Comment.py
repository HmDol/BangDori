from django.db import models


class Comment(models.Model):
    # Article과 유사하게 abstract로 선언후 필요 Article에만 사용
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    writer = models.ForeignKey('CustomerUser', on_delete=models.CASCADE, verbose_name='작성자')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DabangComment(Comment):
    """
    다방 댓글로, Comment를 상속받음
    """
    article_id = models.ForeignKey(
        'DabangArticle', db_column='article_id', on_delete=models.CASCADE, verbose_name='게시글')

    class Meta:
        db_table = 'comment_dabang'
        verbose_name = '다방댓글'
        verbose_name_plural = '다방댓글'


class SuccessionComment(Comment):
    """
    승계 댓글로, Comment를 상속받음
    """
    article_id = models.ForeignKey(
        'SuccessionArticle', db_column='article_id', on_delete=models.CASCADE, verbose_name='게시글')

    class Meta:
        db_table = 'comment_succession'
        verbose_name = '승계댓글'
        verbose_name_plural = '승계댓글'


class EssentialsComment(Comment):
    """
    필수템 댓글로, Comment를 상속받음
    """
    article_id = models.ForeignKey(
        'EssentialsArticle', db_column='article_id', on_delete=models.CASCADE, verbose_name='게시글')

    class Meta:
        db_table = 'comment_essentials'
        verbose_name = '필수템댓글'
        verbose_name_plural = '필수템댓글'


class GroupComment(Comment):
    """
    공동구매 댓글로, Comment를 상속받음
    """
    article_id = models.ForeignKey(
        'GroupArticle', db_column='article_id', on_delete=models.CASCADE, verbose_name='게시글')

    class Meta:
        db_table = 'comment_group'
        verbose_name = '공동구매댓글'
        verbose_name_plural = '공동구매댓글'


class BoardComment(Comment):
    """
    자유 게시판 댓글로, Comment를 상속받음
    """
    article_id = models.ForeignKey(
        'BoardArticle', db_column='article_id', on_delete=models.CASCADE, verbose_name='게시글')

    class Meta:
        db_table = 'comment_board'
        verbose_name = '자유댓글'
        verbose_name_plural = '자유댓글'


class NoticeComment(Comment):
    """
    공지 게시판 댓글로, Comment를 상속받음
    """
    article_id = models.ForeignKey(
        'NoticeArticle', db_column='article_id', on_delete=models.CASCADE, verbose_name='게시글')

    class Meta:
        db_table = 'comment_notice'
        verbose_name = '공지댓글'
        verbose_name_plural = '공지댓글'


class ContactComment(Comment):
    """
    공지 게시판 댓글로, Comment를 상속받음
    """
    article_id = models.ForeignKey(
        'ContactArticle', db_column='article_id', on_delete=models.CASCADE, verbose_name='게시글')

    class Meta:
        db_table = 'comment_contact'
        verbose_name = '문의댓글'
        verbose_name_plural = '문의댓글'
