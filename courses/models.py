from django.db import models
from users.models import User


class Course(models.Model):
    name = models.CharField(max_length=128)

    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    teachers = models.ManyToManyField(User, related_name='teachers_courses')
    students = models.ManyToManyField(User, related_name='students_courses')

    def __str__(self):
        return self.name
