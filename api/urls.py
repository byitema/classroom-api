from django.urls import include, path


urlpatterns = [
    path('users/', include('users.urls')),
    path('', include('courses.urls')),
    path('', include('lectures.urls')),
    path('', include('homeworks.urls')),
    path('', include('solutions.urls')),
    path('', include('marks.urls')),
]
