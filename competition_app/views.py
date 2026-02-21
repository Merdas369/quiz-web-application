from django.shortcuts import render
from django.http import HttpResponse





# Create your views here.


def home(req):
    return HttpResponse("<h1>home page</h1>")


def quiz_start(req, category_id):
    return HttpResponse("<h1>quiz_page</h1>")


def quiz_question(req, quiz_id, num):
    return HttpResponse("<h1>quiz_question</h1>")


def quiz_result(req, quiz_id):
    return HttpResponse("<h1>quiz_result</h1>")


def leaderboard(req):
    return HttpResponse("<h1>leaderboard</h1>")