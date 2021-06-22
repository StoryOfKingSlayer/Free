from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Task, CheckList, Project, CostumUser
from rest_framework.validators import UniqueValidator
import django.contrib.auth.password_validation as validators
from django.core import exceptions
from django.contrib.auth.hashers import make_password
from drf_writable_nested.serializers import WritableNestedModelSerializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password confirm'}
    )

    def create(self, validated_data):
        password = validated_data.get('password')
        validated_data['password'] = make_password(password)
        del validated_data['password_confirm']
        return super(UserSerializer, self).create(validated_data)

    class Meta:
        model = CostumUser
        fields = ['id', 'username', 'password', 'password_confirm', 'role']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class CheckListSerializer(serializers.ModelSerializer):
    task_list = TaskSerializer(many=True, read_only=True)
    ch_user = UserSerializer(many=True, read_only=True)
    class Meta:
        model = CheckList
        fields = ["id", "stepNumber", "project", "user", "task_list", "ch_user"]
        #     [f.name for f in CheckList._meta.fields] + \
        #          ['task_list']
        # read_only_fields = ['task_list']

    # def __init__(self, *args, **kwargs):
    #     super(CheckListSerializer, self).__init__(*args, **kwargs)
    #     request = self.context.get('request')
    #     if request and request.method in ('POST', 'PATCH'):
    #         self.Meta.depth = 0
    #     else:
    #         self.Meta.depth = 1
    #
    # def to_representation(self, instance):
    #     request = self.context.get('request')
    #     response = super().to_representation(instance)
    #     if request and request.method in ('POST', 'PATCH'):
    #         return response
    #     else:
    #         response.get('user').pop('password', None)
    #         return response


class ProjectSerializer(WritableNestedModelSerializer):
    check_lists = CheckListSerializer(many=True, read_only=False)

    class Meta:
        model= Project
        fields = ["id", "projectName", "description", "check_lists"]



# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = '__all__'
