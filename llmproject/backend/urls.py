from django.urls import path
from .views import QuestionAnswerView

urlpatterns = [
     path('question-answer/', QuestionAnswerView.as_view(), name='question_answer'),
]