from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.password_validation import validate_password
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, password, type, first_name, last_name):
        user = self.model(username=username, type=type, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password, type, first_name, last_name):
        user = self.create_user(username, password, type, first_name, last_name)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128, validators=[validate_password])
    type = models.CharField(max_length=64, choices=[('student', 'student'), ('teacher', 'teacher')])
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password', 'type', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
