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
        fields = ['url', 'username', 'email', 'groups', 'password','password_confirm', 'role']

    # def validate(self, data):
    #     password = data.get('password')
    #     if password:
    #         password_confirm = data.get('password_confirm')
    #
    #         if password != password_confirm:
    #             raise serializers.ValidationError("Second Error")
    #     return data


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        read_only_fields = ['Tasks']
        fields = [f.name for f in Task._meta.fields] + \
                 ['Tasks']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class CheckListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckList
        fields = '__all__'

# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = '__all__'
