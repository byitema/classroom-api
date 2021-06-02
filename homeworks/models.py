from django.db import models

from lectures.models import Lecture
from users.models import User


class Homework(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
