from django.urls import path
from .views import home, quiz_start, quiz_result, quiz_question

urlpatterns = [
    path("", home, name= "home"),
    path("quiz_start/<int:category_id>/", quiz_start, name= "quiz_start"),
    path("quiz/<int:quiz_id>/question/<int:num>/", quiz_question, name= "quiz_question"),
    path("quiz/<int:quiz_id>/result/", quiz_result, name= "quiz_result"),
]