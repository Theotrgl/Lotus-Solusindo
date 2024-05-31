from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator
from page1.models import Provinsi, Kota, Kecamatan, Kelurahan, KodePos

# Create your models here.
class Job_Detail(models.Model):
    jenis_pekerjaan = models.CharField(max_length=100)
    kategori_pelayanan = models.CharField(max_length=100)
    jenis_layanan = models.CharField(max_length=100)
    action = models.CharField(max_length=255)

class Hasil(models.Model):
    job_id = models.ForeignKey(Job_Detail, on_delete=models.SET_NULL, null=True)
    keterangan = models.CharField(max_length=255)
    gps = models.CharField(max_length=255, null= True, blank=True)
    ssid = models.CharField(max_length=255, null= True, blank=True)
    signal = models.CharField(max_length=255, null= True, blank=True)
    freq = models.CharField(max_length=255, null= True, blank=True)

class Client(models.Model):
    job_id = models.ForeignKey(Job_Detail, on_delete=models.SET_NULL, null=True)
    nama_client = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null= True, blank=True)

class ClientPIC(models.Model):
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    nama = models.CharField(max_length=255)
    telp = PhoneNumberField()
    email = models.EmailField()

class ClientAlamat(models.Model):
        client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
        provinsi = models.ForeignKey(Provinsi, on_delete=models.CASCADE)
        kota = models.ForeignKey(Kota, on_delete=models.CASCADE)
        kecamatan = models.ForeignKey(Kecamatan, on_delete=models.CASCADE)
        kelurahan = models.ForeignKey(Kelurahan, on_delete=models.CASCADE)
        kode_pos = models.IntegerField (blank=True, null=True, validators=[MaxValueValidator(99999)])
        detail = models.CharField(max_length=500)




