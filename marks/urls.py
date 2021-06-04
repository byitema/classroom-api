from django.urls import path

from . import views


urlpatterns = [
    path('courses/<int:course_pk>/lectures/<int:lecture_pk>/homeworks/<int:homework_pk>/solutions/<int:solution_pk>/'
         'mark/',
         views.MarkView.as_view()),
]
