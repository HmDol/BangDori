import uuid

from django.db import models


def random_filename(instance, name):
    """ 무작위로 파일 이름 생성 """
    return "files/%s.%s" % (uuid.uuid4(), name.split('.')[-1])


class Article(models.Model):
    """
    Article : 게시물 정보를 저장하는 Model

    Parameters
    ----------
    id : AutoField
        Integer 형식의 Auto Increment를 나타내는 PK
    title : CharField
        게시글 제목
    writer : ForeignKey
        작성자, CustomerUser의 username를 FK로 함
        1:N 특성을 가지므로, 계정 삭제시 같이 삭제될 수 있는 CASCADE 특성 사용
    content : TextField
        게시글 내용
    date : DateTimeField
        글 작성 일자, auto_now_add 파라미터를 True로 하여 INSERT시 자동으로 날짜가 생성되는 옵션 사용
    views : PositiveIntegerField
        조회수, 음수가 없으므로 unsigned int 사용
    upvote : PositiveIntegerField
        추천수, 조회수와 마찬가지의 형식 사용
    addr : ForeignKey
        주소 테이블의 ID를 나타냄
    img : ImageField
        게시글의 첨부파일이며, 이미지 경로를 나타냄
    attr : CharField
        게시글이 정렬된 상태를 나타냄
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name='제목')
    writer = models.ForeignKey(
        'CustomerUser', on_delete=models.CASCADE, verbose_name='글쓴이')
    content = models.TextField(verbose_name='내용')
    date = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    views = models.PositiveIntegerField(default=0, verbose_name='조회')
    upvote = models.PositiveIntegerField(default=0, verbose_name='추천')
    addr = models.ForeignKey(
        'Address', on_delete=models.SET_NULL, verbose_name='주소', null=True, default=None)
    img = models.ImageField(upload_to=random_filename, null=True, verbose_name='사진')
    attr = models.CharField(max_length=50, verbose_name='정렬', null=True, default=None)

    def __str__(self):
        # __str__ 오버라이드로 제목만 표시
        return self.title

    def need_addr(self):
        # 주소가 필요한 경우, 해당 메서드를 오버라이드하여 True를 반환
        return False

    def need_sorted_addr(self):
        # 주소 순으로 정렬해야 하는 경우, 해당 메서드를 오버라이드하여 True를 반환
        return False

    def to_dict(self):
        url = self._meta.db_table
        url = url[url.rfind('_') + 1:]
        return {'id': self.id, 'title': self.title, 'writer': self.writer,
                'content': self.content, 'date': self.date, 'views': self.views,
                'upvote': self.upvote, 'need_addr': self.need_addr(), 'url': url,
                'img': self.img}

    class Meta:
        # Meta 클래스 오버라이드로 상세 내용 지정 (Form을 위함)
        abstract = True


class DabangArticle(Article):
    """
    다방 게시판으로, Article을 상속받음
    """

    # 주소 등록이 필요한 게시판
    def need_addr(self):
        return True

    # 주소 정렬이 필요한 게시판
    def need_sorted_addr(self):
        return True

    class Meta:
        db_table = 'article_dabang'
        verbose_name = '다방'
        verbose_name_plural = '다방'


class SuccessionArticle(Article):
    """
    승계 게시판으로, Article을 상속받음
    """

    # 주소 등록이 필요한 게시판
    def need_addr(self):
        return True

    # 주소 정렬이 필요한 게시판
    def need_sorted_addr(self):
        return True

    class Meta:
        db_table = 'article_succession'
        verbose_name = '승계'
        verbose_name_plural = '승계'


class EssentialsArticle(Article):
    """
    필수템 게시판으로, Article을 상속받음
    """

    # 주소 정렬이 필요한 게시판
    def need_sorted_addr(self):
        return True

    class Meta:
        db_table = 'article_essentials'
        verbose_name = '필수템'
        verbose_name_plural = '필수템'


class GroupArticle(Article):
    """
    공동구매 게시판으로, Article을 상속받음
    """

    # 주소 정렬이 필요한 게시판
    def need_sorted_addr(self):
        return True

    class Meta:
        db_table = 'article_group'
        verbose_name = '공동구매'
        verbose_name_plural = '공동구매'


class BoardArticle(Article):
    """
    자유 게시판으로, Article을 상속받음
    """

    class Meta:
        db_table = 'article_board'
        verbose_name = '자유'
        verbose_name_plural = '자유'


class NoticeArticle(Article):
    """
    공지 게시판으로, Article을 상속받음
    """

    class Meta:
        db_table = 'article_notice'
        verbose_name = '공지'
        verbose_name_plural = '공지'


class ContactArticle(Article):
    """
    문의 게시판으로, Article을 상속받음
    """

    class Meta:
        db_table = 'article_contact'
        verbose_name = '문의'
        verbose_name_plural = '문의'
