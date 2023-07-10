import json
import os
import random
import time

import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from bangdori.models import CustomerUser, Authentication
from bangdori.utils import make_signature


class SmsSendView(View):
    def send_sms(self, phone_number, auth_number):
        timestamp = str(int(time.time() * 1000))
        headers = {
            'Content-Type': "application/json; charset=UTF-8",
            'x-ncp-apigw-timestamp': timestamp,
            'x-ncp-iam-access-key': os.getenv('ncloud_private_Accesskey'),
            'x-ncp-apigw-signature-v2': make_signature(timestamp)
        }
        body = {
            "type": "SMS",
            "contentType": "COMM",
            # 사전에 등록해놓은 발신용 번호 입력, 타 번호 입력시 오류
            "from": os.getenv('call_number'),
            "content": f"BangDori에서 보낸 인증번호입니다. [{auth_number}]",  # 메세지를 이쁘게 꾸며보자
            "messages": [{"to": f"{phone_number}"}]
        }
        body = json.dumps(body)
        requests.post(
            'https://sens.apigw.ntruss.com/sms/v2/services/ncp:sms:kr:292652557635:sms_auth/messages', headers=headers,
            data=body)

    def post(self, request):
        # data = json.loads(request.body)
        try:
            input_mobile_num = request.POST['phone_number']
            print(input_mobile_num)
            auth_num = random.randint(10000, 100000)  # 랜덤숫자 생성, 5자리로 계획하였다.
            auth_mobile = Authentication.objects.get(
                phone_number=input_mobile_num)
            auth_mobile.auth_number = auth_num
            auth_mobile.save()
            self.send_sms(
                phone_number=input_mobile_num, auth_number=auth_num)
            return JsonResponse({'message': 'Complete 발송완료'}, status=200)
        except Authentication.DoesNotExist:  # 인증요청번호 미 존재 시 DB 입력 로직 작성
            Authentication.objects.create(
                phone_number=input_mobile_num,
                auth_number=auth_num,
            ).save()
            self.send_sms(phone_number=input_mobile_num, auth_number=auth_num)
            return JsonResponse({'message': '인증번호 발송 및 DB 입력완료'}, status=200)


class SmsVerifyView(View):
    def post(self, request):
        input_mobile_num = request.POST['phone_number']

        message = request.POST['message_number']
        stragety = request.POST['stragety']
        auth_mobile = Authentication.objects.get(
            phone_number=input_mobile_num)
        state = auth_mobile.auth_number == message

        if (stragety == 'verify'):
            if (state):
                return JsonResponse({'message': "Verify Completed!", 'state': 'success'}, status=200)
            else:
                return JsonResponse({'message': "Verify Failed!", 'state': 'failure'}, status=200)

        if (state):
            user = CustomerUser.objects.get(
                phone=input_mobile_num)
            if (user):
                auth_mobile.delete()
                context = {}
                if (stragety == 'findID'):
                    context['id'] = user.username
                    return render(request, 'showID.html', context)
                if (stragety == 'findPW'):
                    context['password'] = user.password
                    return render(request, 'showID.html', context)
            else:
                return JsonResponse({'message': 'Not User!'}, status=200)
        else:
            return JsonResponse({'message': 'Not Correct Number!'}, status=200)
