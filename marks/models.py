from django.db import models

from solutions.models import Solution
from users.models import User


class Mark(models.Model):
    rate = models.IntegerField()

    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)

    def __str__(self):
        return self.rate
