from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer, TaskSerializer, ProjectSerializer, CheckListSerializer
from .models import Task, Project, CheckList, CostumUser


class ShowDependViewSet(viewsets.ModelViewSet):
    queryset = CheckList.objects.all()
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
    serializer_class = CheckListSerializer

    def get_queryset(self):
        if CostumUser.objects.filter(role="Meneger"):
            queriset = self.queryset
        elif CostumUser.objects.filter(role="Executor"):
            queriset = CheckList.objects.all().filter(user=self.request.user)

        return queriset


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions
                          ]


class CheckListViewSet(viewsets.ModelViewSet):
    queryset = CheckList.objects.all().filter()
    serializer_class = CheckListSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CostumUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
