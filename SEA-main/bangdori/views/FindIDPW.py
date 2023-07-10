from django.shortcuts import render


def findID(request):
    return render(request, 'findID.html')


def SMS(request):
    return render(request, 'temp_sms.html')


def SMSPW(request):
    return render(request, 'temp_smsPW.html')


def findPW1(request):
    return render(request, 'findPW1.html')


def findPW2(request):
    return render(request, 'findPW2.html')


def showID(request):
    return render(request, 'showID.html')

def showPW(request):
    return render(request, 'showPW.html')