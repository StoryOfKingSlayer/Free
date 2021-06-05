from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password


class CustomUser(AbstractUser):
    role = models.CharField("Роль", max_length=100)


class Project(models.Model):
    projectName = models.CharField("Название", max_length=150)
    description = models.CharField("Опсианеи", max_length=150, default='SOME STRING')

    def __str__(self):
        return f'{self.id}_{self.projectName}'

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"


class CheckList(models.Model):
    stepNumber = models.CharField("Номер", max_length=100)
    project = models.ForeignKey(Project, verbose_name="Проект", on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(CustomUser, verbose_name="Пользователь", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.id}_{self.stepNumber}'

    class Meta:
        verbose_name = "Чек-лист"
        verbose_name_plural = "Чек-листы"


class Task(models.Model):
    taskName = models.CharField("Задача", max_length=100)
    taskStatus = models.BooleanField(default=False)
    checkList = models.ForeignKey(CheckList, verbose_name="Чек лист", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

