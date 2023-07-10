import hashlib
import hmac
import base64
import os

from django.db.models import QuerySet
from django.template.defaultfilters import register
from dotenv import load_dotenv

from bangdori.models import *
from project.settings import INDEX_ARTICLE_TITLE_COUNT


def make_signature(timestamp):
    load_dotenv()

    access_key = os.getenv('ncloud_private_Accesskey')
    secret_key = os.getenv('ncloud_private_Secretkey')

    secret_key = bytes(secret_key, 'UTF-8')

    uri = "/sms/v2/services/ncp:sms:kr:292652557635:sms_auth/messages"
    # uri 중간에 Console - Project - 해당 Project 서비스 ID 입력 (예시 = ncp:sms:kr:263092132141:sms)

    message = "POST" + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(
        hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())

    return signingKey


def getCommentModelByName(name):
    comments = None
    if name == 'board':
        comments = BoardComment
    elif name == 'dabang':
        comments = DabangComment
    elif name == 'succession':
        comments = SuccessionComment
    elif name == 'essentials':
        comments = EssentialsComment
    elif name == 'notice':
        comments = NoticeComment
    elif name == 'contact':
        comments = ContactComment
    elif name == 'group':
        comments = GroupComment

    return comments


def getModelByName(name, is_all=False):
    """
    getModelByName : name에 따라 적절한 Model 객체를 반환하는 클래스

    Parameters
    ----------
    name : url에 사용된 이름
    is_all : 모든 객체를 가져올지 결정
    """

    articles = None

    # URL로부터 넘겨받은 게시판 유형에 따라 다른 context 전달
    if name == 'board':
        articles = BoardArticle
    elif name == 'dabang':
        articles = DabangArticle
    elif name == 'succession':
        articles = SuccessionArticle
    elif name == 'essentials':
        articles = EssentialsArticle
    elif name == 'notice':
        articles = NoticeArticle
    elif name == 'contact':
        articles = ContactArticle
    elif name == 'group':
        articles = GroupArticle
    elif is_all:
        articles = [BoardArticle, DabangArticle, SuccessionArticle,
                    EssentialsArticle, NoticeArticle, ContactArticle, GroupArticle]

    return articles


def getArticlesByAddress(user: CustomerUser, articles: QuerySet):
    try:
        # addr : 게시글을 Key로, 사용자와의 거리를 Value로 가지는 dict
        addr = {article: user.addr.calcDistance(
            article.addr) for article in articles}
    except:
        return articles

    # 거리가 가까운 순으로 정렬
    addr = {k: v for k, v in sorted(addr.items(), key=lambda x: x[1])}

    # list로 변환하여 반환
    return list(addr.keys())


def getAllArticles():
    # 모든 게시판 객체 가져옴
    boards = getModelByName(None, True)

    result = list()
    for board in boards:
        articles = board.objects.all().filter()
        # 게시글이 없는 게시판은 제외
        if articles.count() > 0:
            for article in articles:
                # dict로 변환하여 저장
                result.append(article.to_dict())

    return result


@register.filter(name='dict_key')
def dictKey(d, k):
    """
    Django Template에서 Dict의 Key를 통해 Value를 얻고자 하는
    Template용 함수
    """
    return d[k]


def addCommentsToTitle(articles: list, name=None):
    """
    Index에 출력할 게시글 목록 위젯에 사용됨
    게시글 제목의 댓글 수를 '제목 [댓글수]' 형식으로 만들어줌

    Parameters
    ----------
    articles : list
        게시글의 정보인 Article을 dict 형식으로 저장한 후, 이를 list로 만듬
    name : str
        게시판 이름({{ url }})을 가져옴. 만약 지정되어 있지 않다면(=None),
        게시판 내에 포함된 변수를 이용하여 getCommentModelByName 함수를 매번 호출함. (핫, 최근 게시물)
        그렇지 않고, 게시판이 특정되어 있다면 getCommentModelByName를 매번 호출하지 않고,
        로드 시간을 아낄 수 있으므로 해당 파라미터를 이용

    Returns
    ----------
    articles의 모든 항목(Article)의 'title' 변수에 댓글 수가 추가된 변수 (dict로 구성된 list)
    """
    # Comment Model을 특정할 수 있을 경우, 코드 중복을 막기 위해 미리 가져옴
    cut = INDEX_ARTICLE_TITLE_COUNT
    model = None
    if name is not None:
        model = getCommentModelByName(name).objects.all()

    for a in articles:
        if a.get('comment_added', None):
            continue

        if name is not None:
            # 이름이 특정된 경우, 미리 가져온 Model에서 갯수를 가져옴
            count = model.filter(article_id=a['id']).count()
        else:
            # 이름이 특정되지 않은 경우, url 변수를 이용하여 Model을 가져온 뒤, 갯수를 가져옴
            count = getCommentModelByName(a['url']).objects.all().filter(article_id=a['id']).count()

        # list에 포함된 각 title을 가져옴
        title = a['title']

        if len(a['title']) > cut:
            # 글자수 자르기 적용
            title = title[:cut]
            title = f'{title}...'
            a['title'] = title

        # 해당 게시글에 댓글이 있는 경우에만 추가해 줌
        if count > 0:
            a['title'] = f'{title} [{count}]'
            a['comment_added'] = True

    return articles
