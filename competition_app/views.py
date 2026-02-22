from itertools import count
from django.contrib.auth import user_logged_in
from django.shortcuts import render, redirect
from django.http import HttpResponse
from competition_app.models import Category, Question, Answer, QuizSession, UserAnswer
from django.contrib.auth.models import User
from competition_app.api_handler import get_questions_from_api
import datetime as td





# Create your views here.


def home(req):
    return HttpResponse("<h1>home page</h1>")


def quiz_start(req, category_id):
    # getting the result dictionary from the api
    result = get_questions_from_api(category_id)
    # making the new session for the quiz
    category = Category.objects.get(category_id=category_id)
    quiz_session = QuizSession.objects.create(user= req.user if req.user.is_authenticated else None,
                               category= category,
                               score= 0, total_question= 10,
                               completed_at= None,
                               is_completed= False)
    # saving the all 10 questions in the question model
    for q in range(10):
       question, created = Question.objects.get_or_create(category= category,
                                question= result[q]["question"], difficulty= result[q]["difficulty"],
                                type= result[q]["type"])
    # saving the answers in answer model correct answer and the 3 remain incorrect answer
       for i in range(4):
           Answer.objects.create(question= question,
                answer_text= result[q]["all_answer"][i],
                is_correct= True if result[q]["all_answer"][i] == result[q]["correct_answer"] else False)
    return redirect("quiz_question", quiz_id= quiz_session.id, num= 1)


def quiz_question(req, quiz_id, num):
    return HttpResponse("<h1>quiz_question</h1>")


def quiz_result(req, quiz_id):
    return HttpResponse("<h1>quiz_result</h1>")


def leaderboard(req):
    return HttpResponse("<h1>leaderboard</h1>")