from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

def funky(request):
    response="""<html><body><p>This is the funky function sample</p>
    <body><html>"""
    return HttpResponse(response)


