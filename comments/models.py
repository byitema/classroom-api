from django.db import models

from marks.models import Mark
from users.models import User


class Comment(models.Model):
    text = models.TextField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
