from django.shortcuts import render


def home(request):
    print(request.COOKIES)
    return render(request, 'home/index.html', context={})