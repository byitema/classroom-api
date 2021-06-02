from django.db import models

from homeworks.models import Homework
from users.models import User


class Mark(models.Model):
    rate = models.IntegerField()

    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)

    def __str__(self):
        return self.rate
