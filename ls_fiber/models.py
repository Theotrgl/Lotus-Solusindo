from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator
from page1.models import Provinsi, Kota, Kecamatan, Kelurahan
from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):
    namaPelanggan = models.CharField(max_length=255, null=True)
    nomorTelponPelanggan = PhoneNumberField(null=True, blank=True)

    def __str__(self):
        return self.namaPelanggan


class ClientPIC(models.Model):
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    namaPIC = models.CharField(max_length=255, null=True, blank=True)
    nomorTelponPIC = PhoneNumberField(null=True, blank=True)
    # email = models.EmailField()

    def __str__(self):
        return self.namaPIC
    
class ClientAlamat(models.Model):
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    provinsi = models.CharField(max_length=500, null=True)
    kota = models.CharField(max_length=500, null=True)
    kecamatan = models.CharField(max_length=500, null=True)
    kelurahan = models.CharField(max_length=500, null=True)
    kodePos = models.IntegerField (blank=True, null=True, validators=[MaxValueValidator(99999)])
    detailAlamat = models.CharField(max_length=500, null=True, blank= True)

    def __str__(self):
        return self.detailAlamat
    
class Worker(models.Model):
    nama = models.CharField(max_length=255)
    ktp = models.IntegerField(null=True)
    telponWorker = PhoneNumberField(null=True)
    rekening = models.IntegerField(null=True)
    
    def __str__(self):
        return self.nama
class JobDetail(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    tanggal = models.DateField(null=True)
    jenisPekerjaan = models.CharField(max_length=100)
    kategoriPekerjaan = models.CharField(max_length=100)
    jenisLayanan = models.CharField(max_length=100)
    action = models.CharField(max_length=255)
    keterangan = models.CharField(max_length=255, null=True)
    gps = models.CharField(max_length=255, null= True, blank=True)
    ssid = models.CharField(max_length=255, null= True, blank=True)
    signal = models.CharField(max_length=255, null= True, blank=True)
    freq = models.CharField(max_length=255, null= True, blank=True)
    status = models.CharField(max_length=500, null=True, blank=True)
    perangkatInstall = models.CharField(max_length=255, null=True, blank=True)
    perangkatDismantle = models.CharField(max_length=255, null=True, blank=True)
    jamMulai = models.TimeField(null = True)
    jamSelesai = models.TimeField(null = True)
    lampiran = models.ImageField(upload_to='fiber_photos/', null=True)
    lampiran_og = models.ImageField(upload_to = 'fiber_photos/', null=True)
    pelaksanaPekerjaan = models.TextField(max_length = 1000, null = True, blank = True)
    timestamp = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.sender}-{self.timestamp}'
    
class JobWorkers(models.Model):
    job = models.ForeignKey(JobDetail, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)

