from django.http import HttpResponse
from django.shortcuts import render

def index(rewuest):
    return render()


def about(rewuest):
    return HttpResponse('About Page')
