from django.urls import path

from . import views


urlpatterns = [
    path('courses/<int:course_pk>/lectures/<int:lecture_pk>/homeworks/', views.HomeworkList.as_view()),
    path('courses/<int:course_pk>/lectures/<int:lecture_pk>/homeworks/<int:pk>/', views.HomeworkDetail.as_view()),
]
