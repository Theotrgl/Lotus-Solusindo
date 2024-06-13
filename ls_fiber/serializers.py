from rest_framework import serializers
from django.contrib.auth.models import User
import json

from .models import *
from page1.models import Provinsi, Kota, Kecamatan, Kelurahan, KodePos

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

class ClientNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['namaPelanggan']

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
    pelaksanaPekerjaan = serializers.PrimaryKeyRelatedField(queryset=Worker.objects.all(), many=True)
    lampiran = serializers.ImageField()
    class Meta:
        model = JobDetail
        fields = '__all__' 

class ProvinsiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provinsi
        fields = '__all__'

class KotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kota
        fields = '__all__'

class KecamatanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kecamatan
        fields = '__all__'

class KelurahanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kelurahan
        fields = '__all__'

class KodePosSerializer(serializers.ModelSerializer):
    class Meta:
        model = KodePos
        fields = '__all__'
