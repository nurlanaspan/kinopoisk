from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, mal!<br>If you are pidor, go <a href='http://127.0.0.1:8000/pidor'>here</a>")

def pidor(request):
    return HttpResponse("Hello, <p style='color: red'>pidor!</p>")
# Create your views here.
