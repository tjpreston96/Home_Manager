from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.

# Home
def home(request):
    return HttpResponse("<h1>Hello /ᐠ｡‸｡ᐟ\ﾉ</h1>")


# About
def about(request):
    return render(request, "about.html")
