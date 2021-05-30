from django.contrib import admin
from .models import Comment, Course, Homework, Lecture, Mark, Solution


admin.site.register(Comment)
admin.site.register(Course)
admin.site.register(Homework)
admin.site.register(Lecture)
admin.site.register(Mark)
admin.site.register(Solution)
