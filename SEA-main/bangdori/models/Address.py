import math

from django.db import models


class Address(models.Model):
    """
    주소를 저장하는 Model

    Parameters
    ----------
    id : AutoField
        Integer 형식의 Auto Increment를 나타내는 PK
    postcode : IntegerField
        우편번호 (예시 : 13536)
    road : CharField
        도로명 주소 (예시 : 경기 성남시 분당구 판교역로 235)
    lot : CharField
        지번 주소 (예시 : 경기 성남시 분당구 삼평동 681)
    detail : CharField
        상세 주소
    extra : CharField
        도/시 이름 (예시 : 경기)
    state : CharField
        시/군/구 이름 (예시 : 성남시 분당구)
    road_name : CharField
        도로명 값, 검색 결과 중 선택한 도로명주소의 "도로명" 값
    lat : FloatField
        위도
    lng : FloatField
        경도
    """
    id = models.AutoField(primary_key=True)
    postcode = models.IntegerField(
        verbose_name='우편번호', null=True, default=None)
    road = models.CharField(
        max_length=50, verbose_name='도로명주소', null=True, default=None)
    lot = models.CharField(
        max_length=50, verbose_name='지번주소', null=True, default=None)
    detail = models.CharField(
        max_length=50, verbose_name='상세주소', null=True, default=None)
    extra = models.CharField(
        max_length=50, verbose_name='참고항목', null=True, default=None)
    city = models.CharField(
        max_length=10, verbose_name='도/시 이름', null=True, default=None)
    state = models.CharField(
        max_length=10, verbose_name='시/군/구 이름', null=True, default=None)
    road_name = models.CharField(
        max_length=10, verbose_name='도로명', null=True, default=None)
    lat = models.FloatField(verbose_name='위도', null=False)
    lng = models.FloatField(verbose_name='경도', null=False)

    def getTags(self):
        # 카카오에서 제공하는 data에 해당하는 Model 변수 이름 dict 반환
        return {'postcode': 'postcode', 'road': 'road', 'lot': 'jibun',
                'detail': 'detail', 'extra': 'extra', 'city': 'sido',
                'state': 'sigungu', 'road_name': 'roadname'}

    def __str__(self):
        return f'{self.road}{self.extra} {self.detail}'

    def createFromPost(self, request):
        # WSGIRequest를 통해 데이터를 받아와서 만들어줌
        try:
            self.postcode = int(request.POST.get('postcode'))
        except:
            pass

        self.road = request.POST.get('road')
        self.lot = request.POST.get('lot')
        self.detail = request.POST.get('detail')
        self.extra = request.POST.get('extra')
        self.city = request.POST.get('sido')
        self.state = request.POST.get('sigungu')
        self.road_name = request.POST.get('roadname')
        self.lat = float(request.POST.get('lat'))
        self.lng = float(request.POST.get('lng'))

        # 주소 모델 저장
        self.save()

        return self

    def calcDistance(self, another):
        # another 파라미터로 전달받은 다른 객체와의 거리를 계산
        # 경도 Lat, 위도 Lng과의 직선 거리 차이를 계산하여 출력함

        # 점과 점 사이의 거리이므로, 피타고라스 정리 이용
        return math.sqrt(math.pow(another.lat - self.lat, 2) + math.pow(another.lng - self.lng, 2))
