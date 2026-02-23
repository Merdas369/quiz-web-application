from django.db import models
from django.conf import settings

# Create your models here.


class Category(models.Model):

    name = models.CharField(max_length= 25)
    category_id = models.IntegerField(unique= True)

    def __str__(self):
        return self.name


class Question(models.Model):

    category = models.ForeignKey(Category, on_delete= models.CASCADE)
    question = models.TextField(unique= True)
    difficulty = models.CharField(max_length=10)
    type = models.CharField(max_length=10)

    def __str__(self):
        return self.question

class Answer(models.Model):

    question = models.ForeignKey(Question, on_delete= models.CASCADE)
    answer_text = models.TextField()
    is_correct = models.BooleanField()

    def __str__(self):
        return f"{self.answer_text} ({'✓' if self.is_correct else '✗'})"

class QuizSession(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, null= True, blank= True)
    category = models.ForeignKey(Category, on_delete= models.CASCADE)
    questions = models.ManyToManyField(Question)
    score = models.IntegerField()
    total_question = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add= True)
    completed_at = models.DateTimeField(null= True, blank= True)
    is_completed = models.BooleanField(default= False)

    def __str__(self):
        return f"Quiz #{self.id} - {self.category.name} - Score: {self.score}/{self.total_question}"

class UserAnswer(models.Model):

    quiz_session = models.ForeignKey(QuizSession, on_delete= models.CASCADE)
    question = models.ForeignKey(Question, on_delete= models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete= models.CASCADE)
    is_correct = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f"Answer for Quiz #{self.quiz_session.id} - {'✓' if self.is_correct else '✗'}"
