from django.db import models

from courses.models import Course
from users.models import User


class Lecture(models.Model):
    name = models.CharField(max_length=128)
    presentation = models.FileField(upload_to='uploads/')
    description = models.TextField()

    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name