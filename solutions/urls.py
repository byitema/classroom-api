from django.urls import path

from . import views


urlpatterns = [
    path('courses/<int:course_pk>/lectures/<int:lecture_pk>/homeworks/<int:homework_pk>/solutions/',
         views.SolutionList.as_view()),
    path('courses/<int:course_pk>/lectures/<int:lecture_pk>/homeworks/<int:homework_pk>/solutions/<int:pk>',
         views.SolutionDetail.as_view())
]
