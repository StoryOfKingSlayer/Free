from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission


# Create your models here.
class CostumUser(AbstractUser):
    role = models.CharField("Роль", max_length=100)

    def save(self, *args, **kwargs):
        super(CostumUser, self).save(*args, **kwargs)
        permissions = []
        if self.role == "Executor":
            permissions = [
                Permission.objects.get(name='Can view Чек-лист'),
            ]
        elif self.role == "Meneger":
            permissions = [
                Permission.objects.get(name='Can view Проект'),
                Permission.objects.get(name='Can add Проект'),
                Permission.objects.get(name='Can change Проект'),
                Permission.objects.get(name='Can delete Проект'),
                Permission.objects.get(name='Can view Чек-лист'),
                Permission.objects.get(name='Can add Чек-лист'),
                Permission.objects.get(name='Can change Чек-лист'),
                Permission.objects.get(name='Can delete Чек-лист'),
                Permission.objects.get(name='Can view Задача'),
                Permission.objects.get(name='Can add Задача'),
                Permission.objects.get(name='Can change Задача'),
                Permission.objects.get(name='Can delete Задача'),
                Permission.objects.get(name='Can view user'),
                Permission.objects.get(name='Can add user'),
                Permission.objects.get(name='Can delete user'),
                Permission.objects.get(name='Can change user'),
            ]
        self.user_permissions.set(permissions)


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
    user = models.ForeignKey(CostumUser, verbose_name="Пользователь", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.id}_{self.stepNumber}'

    class Meta:
        verbose_name = "Чек-лист"
        verbose_name_plural = "Чек-листы"


class Task(models.Model):
    taskName = models.CharField("Задача", max_length=100)
    taskStatus = models.BooleanField(default=False)
    checkList = models.ForeignKey(CheckList, verbose_name="Чек лист", on_delete=models.CASCADE,
                                  related_name="task_list")

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     birth_date = models.DateField(null=True, blank=True)
#     role = models.CharField("Роль", max_length=100)
#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
