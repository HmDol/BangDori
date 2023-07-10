import django
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomerUser(AbstractUser):
    """
    CustomerUser : 사용자 정보를 저장하는 Model

    Parameters
    ----------
    email : CharField
        이메일
    birthday : DateField
        생일
    phone : CharField
        전화번호
    nickname : CharField
        닉네임
    addr : ForeignKey
        주소 테이블의 ID를 나타냄
    provider : CharField
        Local Login , Social Login 구분자
    blocked_at : DateTimeField
        (예정 : is_active 필드와 함께 작동) 사용자가 비활성화된 날짜를 알려줌
    corp_num : CharField
        사업자 등록번호
    """

    email = models.CharField(
        max_length=30, db_column='email', verbose_name='email', blank=True)
    birthday = models.DateField(
        default=django.utils.timezone.now, db_column='birth', verbose_name='birth', null=True)
    phone = models.CharField(
        max_length=30, db_column='phone', verbose_name='phone')
    nickname = models.CharField(
        max_length=30, db_column='nickname', verbose_name='nickname', blank=True)
    addr = models.ForeignKey(
        'Address', on_delete=models.SET_NULL, verbose_name='address', null=True, default=None)
    provider = models.CharField(
        max_length=30, db_column='provider', verbose_name='provider', null=True)
    blocked_at = models.DateTimeField(
        db_column='blocked_at', null=True, default=None)
    corp_num = models.CharField(
        max_length=30, verbose_name='corp_num', null=True, default=None)
    mileage = models.PositiveIntegerField(verbose_name='mileage', default=0)

    def __str__(self):
        return self.username
