from django.urls import include, path
from api import views


urlpatterns = [
    path('users/', include('users.urls')),

    path('courses/', views.CourseList.as_view()),
    path('courses/<int:pk>/', views.CourseDetail.as_view()),

    path('courses/<int:course_pk>/add_user/<int:user_pk>/', views.CourseUsers.as_view()),

    path('courses/<int:course_pk>/lectures/', views.LectureList.as_view()),
    path('courses/<int:course_pk>/lectures/<int:pk>/', views.LectureDetail.as_view()),

    path('courses/<int:course_pk>/lectures/<int:lecture_pk>/homeworks/', views.HomeworkList.as_view()),
    path('courses/<int:course_pk>/lectures/<int:lecture_pk>/homeworks/<int:pk>', views.HomeworkDetail.as_view()),
]
