import uuid

from django.db import models
from django.conf import settings


# Create your models here.

def random_profile_img(instance, name):
    """ 무작위로 파일 이름 생성 """
    return "profile/%s.%s" % (uuid.uuid4(), name.split('.')[-1])

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to=random_profile_img, null=True)
