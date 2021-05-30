from django.db import models
from users.models import User


class Course(models.Model):
    name = models.CharField(max_length=128)

    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    teachers = models.ManyToManyField(User, related_name='teachers')
    students = models.ManyToManyField(User, related_name='students')

    def __str__(self):
        return self.name


class Lecture(models.Model):
    name = models.CharField(max_length=128)
    presentation = models.FileField(upload_to='uploads/')
    description = models.TextField()

    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Homework(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Solution(models.Model):
    text = models.TextField()

    students = models.ForeignKey(User, on_delete=models.CASCADE)
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Mark(models.Model):
    rate = models.IntegerField()

    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)

    def __str__(self):
        return self.rate


class Comment(models.Model):
    text = models.TextField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
