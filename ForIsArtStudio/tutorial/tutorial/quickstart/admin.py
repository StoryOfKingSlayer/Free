from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import Project, CheckList, Task, CostumUser


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'projectName', 'description')


class CheckListAdmin(admin.ModelAdmin):
    list_display = ('id', 'stepNumber', 'project', 'user')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'taskName', 'taskStatus', 'checkList')


# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'birth_date', 'role')

# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'role')


# admin.site.register(CostumUser, CustomUserAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(CheckList, CheckListAdmin)
admin.site.register(Task, TaskAdmin)


@admin.register(CostumUser)
class CostumUserModelAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + \
                (
                    (
                        'Дополнительные поля', {
                            'fields': (
                                'role',
                            )
                        }
                    ),
                )
