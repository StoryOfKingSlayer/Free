from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer, TaskSerializer, ProjectSerializer, CheckListSerializer
from .models import Task, Project, CheckList, CostumUser
from .permission_classes import IsAdminOrManager





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
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions,
    ]
    serializer_class = ProjectSerializer
    def get_queryset(self):
        queryset = Project.objects.all()
        user = self.request.user
        if user.role == "Executor":
            queryset = Project.objects.filter(id__in=CheckList.objects.values("project_id").filter(
                user_id__in=CostumUser.objects.filter(id=self.request.user.id)))
        return queryset


class CheckListViewSet(viewsets.ModelViewSet):
    queryset = CheckList.objects.all()
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
    serializer_class = CheckListSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == "Meneger" or user.role == "Admin":
            queriset = self.queryset
        elif user.role == "Executor":
            queriset = CheckList.objects.filter(user=self.request.user)
        return queriset


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CostumUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
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
