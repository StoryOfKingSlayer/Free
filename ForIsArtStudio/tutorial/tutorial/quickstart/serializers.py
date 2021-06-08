from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Task, CheckList, Project, CostumUser
from rest_framework.validators import UniqueValidator
import django.contrib.auth.password_validation as validators
from django.core import exceptions
from django.contrib.auth.hashers import make_password


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
        fields = ['url', 'username', 'email', 'groups', 'password', 'password_confirm', 'role']



class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class CheckListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckList
        fields = [f.name for f in CheckList._meta.fields] + \
                 ['task_list']
        read_only_fields = ['task_list']

    def __init__(self, *args, **kwargs):
        super(CheckListSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method in ('POST', 'PATCH'):
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1

    def to_representation(self, instance):
         request = self.context.get('request')
         response = super().to_representation(instance)
         if request and request.method in ('POST', 'PATCH'):
             return response
         else:
            response.get('user').pop('password', None)
            return response



# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = '__all__'
