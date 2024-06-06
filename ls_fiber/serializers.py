from rest_framework import serializers
from django.contrib.auth.models import User
import json

from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'first_name','email', 'password']

        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'  # Adjust fields as needed

class ClientPICSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientPIC
        fields = '__all__'  # Adjust fields as needed

class ClientAlamatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientAlamat
        fields = '__all__'  # Adjust fields as needed

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = '__all__'

class JobDetailSerializer(serializers.ModelSerializer):
    pelaksanaPekerjaan = serializers.ListField(
        child=serializers.CharField(max_length=1000),
        allow_empty= False
    )
    lampiran = serializers.ImageField()
    class Meta:
        model = JobDetail
        fields = '__all__' 
