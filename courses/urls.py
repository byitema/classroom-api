from django.urls import path

from . import views


urlpatterns = [
    path('courses/', views.CourseList.as_view()),
    path('courses/<int:pk>/', views.CourseDetail.as_view()),

    path('courses/<int:course_pk>/add_user/<int:user_pk>/', views.CourseUsers.as_view()),
]
