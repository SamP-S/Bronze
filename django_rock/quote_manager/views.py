from django.shortcuts import render
from django.http import HttpResponse

def quotes_view(request):
    return HttpResponse("Hello, World!")

