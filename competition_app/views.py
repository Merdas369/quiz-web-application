from django.shortcuts import render, redirect
from django.http import HttpResponse
from competition_app.models import Category, Question, Answer, QuizSession, UserAnswer
from competition_app.api_handler import get_questions_from_api
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone



# Create your views here.


def home(req):
    context = {"categories": Category.objects.all()}
    # for category in categories:
    #     url = reverse('quiz_start', kwargs={'category_id': category.category_id})
    #     html += f"<a href='{url}'><button>{category.name}</button></a><br><br>"

    return render(req, "competition_app/home_page.html", context)


def quiz_start(req, category_id):
    # getting the result dictionary from the api
    result = get_questions_from_api(category_id)
    if len(result) < 10:
        return HttpResponse(f"خطا: فقط {len(result)} سوال دریافت شد! باید ۱۰ تا باشه. لطفاً دوباره تلاش کنید.")
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
def quiz_question(request, quiz_id, num):
    quiz_session = QuizSession.objects.get(id=quiz_id)
    questions = quiz_session.questions.all().order_by('id')
    question = questions[num - 1]
    answers = Answer.objects.filter(question=question)

    if request.method == "GET":
        context = {
            'quiz_session': quiz_session,
            'question': question,
            'answers': answers,
            'num': num,
        }

        return render(request, 'competition_app/quiz_question.html', context)

    elif request.method == "POST":
        answer_id = request.POST.get('answer_id')
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


def quiz_result(request, quiz_id):
    # Get the quiz session
    quiz_session = QuizSession.objects.get(id=quiz_id)

    # Count correct answers
    correct_answers = UserAnswer.objects.filter(
        quiz_session=quiz_session,
        is_correct=True
    ).count()

    # Update quiz session
    quiz_session.score = correct_answers
    quiz_session.completed_at = timezone.now()
    quiz_session.is_completed = True
    quiz_session.save()

    # Calculate percentage
    percentage = (correct_answers / 10) * 100

    # Determine performance message
    if percentage >= 90:
        message = "Outstanding! You're a trivia master!"
        emoji = "🏆"
    elif percentage >= 70:
        message = "Great job! You know your stuff!"
        emoji = "🎉"
    elif percentage >= 50:
        message = "Good effort! Keep learning!"
        emoji = "👍"
    else:
        message = "Don't give up! Practice makes perfect!"
        emoji = "💪"

    context = {
        'quiz_session': quiz_session,
        'correct_answers': correct_answers,
        'total_questions': 10,
        'percentage': percentage,
        'message': message,
        'emoji': emoji,
    }

    return render(request, 'competition_app/quiz_result.html', context)