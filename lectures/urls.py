from django.urls import path

from . import views


urlpatterns = [
    path('courses/<int:course_pk>/lectures/', views.LectureList.as_view()),
    path('courses/<int:course_pk>/lectures/<int:pk>/', views.LectureDetail.as_view()),
]
