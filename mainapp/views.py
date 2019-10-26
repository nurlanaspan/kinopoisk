from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, mal!")

def pidor(request):
    return HttpResponse("Hello, <p style='color: red'>pidor!</p>")
# Create your views here.
