from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer, TaskSerializer, ProjectSerializer, CheckListSerializer
from .models import Task, Project, CheckList, CostumUser
from .permission_classes import IsAdminOrManager
from django.http import HttpResponse


# class ShowProjectForMA(viewsets.ModelViewSet):
#     permission_classes = [
#         permissions.IsAuthenticated,
#         permissions.DjangoModelPermissions,
#     ]
#     serializer_class = ProjectSerializer
#
#     def get_queryset(self):
#         queryset = Project.objects.all()
#         user = self.request.user
#         if user.role == "Executor":
#             queryset = Project.objects.filter(id__in=CheckList.objects.values("project_id").filter(user_id__in=CostumUser.objects.filter(id=self.request.user.id)))
#         return queryset


# class ShowDependViewSet(viewsets.ModelViewSet):
#     queryset = CheckList.objects.all()
#     permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
#     serializer_class = CheckListSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         if user.role == "Meneger" or user.role == "Admin":
#             queriset = self.queryset
#         elif user.role == "Executor":
#             queriset = CheckList.objects.filter(user=self.request.user)
#         return queriset


class TaskViewSet(viewsets.ModelViewSet):
    pagination_class = None

    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        queryset = Task.objects.all()
        user = self.request.user
        if user.role == "Executor":
            queryset = Task.objects.filter(checkList__in=CheckList.objects.values("id"))
        return queryset


class ProjectViewSet(viewsets.ModelViewSet):
    pagination_class = None
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions,
    ]
    serializer_class = ProjectSerializer

    def get_queryset(self):

        user = self.request.user
        queryset = Project.objects.all()
        to_be_deleted = []
        for p in queryset:
            check_lists_status = []
            for cl in p.check_lists.all():
                if all(t.taskStatus for t in cl.task_list.all()):
                    check_lists_status.append(True)
                else:
                    check_lists_status.append(False)
            if len(CheckList.objects.all()) != 0:
                if all(check_lists_status):
                    to_be_deleted.append(p.id)
        queryset.filter(id__in=to_be_deleted).delete()

        if user.role == "Executor":
            queryset = Project.objects.filter(id__in=CheckList.objects.values("project_id").filter(
                user_id__in=CostumUser.objects.filter(id=self.request.user.id)))

        return queryset


class CheckListViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = CheckList.objects.all()
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
    serializer_class = CheckListSerializer
    def get_queryset(self):
        queryset = CheckList.objects.all()
        to_be_deleted = []
        for cl in queryset:
            if len(cl.task_list.all()) != 0:
                if all(t.taskStatus for t in cl.task_list.all()):
                    to_be_deleted.append(cl.id)
        queryset.filter(id__in=to_be_deleted).delete()
        user = self.request.user
        if user.role == "Meneger" or user.role == "Admin":
            queryset = CheckList.objects.all()
        elif user.role == "Executor":
            queryset = CheckList.objects.filter(user=self.request.user)
        return queryset

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CostumUser.objects.all().order_by('-date_joined')
    pagination_class = None
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        queryset = CostumUser.objects.all()
        user = self.request.user
        if (user.role == "Executor"):
            queryset = CostumUser.objects.filter(id=self.request.user.id)
        return queryset


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
