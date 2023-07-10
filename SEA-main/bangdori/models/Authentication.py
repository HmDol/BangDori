from django.db import models


class Authentication(models.Model):
    phone_number = models.CharField('휴대폰 번호', max_length=30)
    auth_number = models.CharField('인증번호', max_length=30)

    class Meta:
        db_table = 'authentications'  # DB 테이블명
        verbose_name_plural = "휴대폰인증 관리 페이지"  # Admin 페이지에서 나타나는 설명
