from itertools import count
from django.contrib.auth import user_logged_in
from django.shortcuts import render, redirect
from django.http import HttpResponse
from competition_app.models import Category, Question, Answer, QuizSession, UserAnswer
from django.contrib.auth.models import User
from competition_app.api_handler import get_questions_from_api
from django.urls import reverse
import requests
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone





# Create your views here.


def home(req):
    categories = Category.objects.all()

    html = "<h1>choose a category:</h1>"

    for category in categories:
        url = reverse('quiz_start', kwargs={'category_id': category.category_id})
        html += f"<a href='{url}'><button>{category.name}</button></a><br><br>"

    return HttpResponse(html)


def quiz_start(req, category_id):
    # getting the result dictionary from the api
    result = get_questions_from_api(category_id)
    # making the new session for the quiz
    category = Category.objects.get(category_id=category_id)
    quiz_session = QuizSession.objects.create(
        user=req.user if req.user.is_authenticated else None,
        category= category,
        score= 0,
        total_question= 10
    )
    # saving the all 10 questions in the question model
    for question_data in result:
        question= Question.objects.create(
            question=question_data["question"],
                category= category,
                difficulty= question_data["difficulty"],
                type= question_data.get("type", "multiple")
        )
    # making the relationship between the session and the questions
        quiz_session.questions.add(question)
    # saving the answers in answer model correct answer and the 3 remain incorrect answer if any question is create
        for answer_text in question_data["all_answer"]:
            is_correct = (answer_text == question_data["correct_answer"])
            Answer.objects.create(
                question=question,
                answer_text=answer_text,
                is_correct=is_correct
            )
    return redirect("quiz_question", quiz_id= quiz_session.id, num= 1)

@csrf_exempt
def quiz_question(req, quiz_id, num):

    quiz_session = QuizSession.objects.get(id=quiz_id)
    questions = quiz_session.questions.all().order_by('id')
    question = questions[num - 1]

    if req.method == "GET":
        answers = Answer.objects.filter(question=question)
        text = f"<h2>Question {num} from 10:</h2>"
        text += f"<p>{question.question}</p>"
        text += f"<form method='POST'>"

        for answer in answers:
            text += f"<input type='radio' name='answer_id' value='{answer.id}'> {answer.answer_text}<br>"

        text += "<br><button type='submit'>submit and continue</button>"
        text += "</form>"

        return HttpResponse(text)

    elif req.method == "POST":
        answer_id = req.POST.get('answer_id')
        selected_answer = Answer.objects.get(id=answer_id)

        UserAnswer.objects.create(
            quiz_session=quiz_session,
            question=question,
            selected_answer=selected_answer,
            is_correct=selected_answer.is_correct
        )

        if num == 10:
            return redirect('quiz_result', quiz_id=quiz_session.id)
        else:
            return redirect('quiz_question', quiz_id=quiz_session.id, num=num + 1)

def quiz_result(req, quiz_id):

    # finding the quiz session
    quiz_session = QuizSession.objects.get(id= quiz_id)

    # finding the user's answers and counting the correct answers
    user_true_answers = UserAnswer.objects.filter(quiz_session= quiz_session, is_correct= True).count()

    # updating the quiz_session
    QuizSession.objects.filter(id= quiz_id).update(score= user_true_answers, completed_at= timezone.now(),
                                is_completed= True)

    return HttpResponse(f"<h2>you'r score is: {user_true_answers} from 10.")