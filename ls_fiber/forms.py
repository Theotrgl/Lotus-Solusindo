from django import forms
from django.forms import widgets
from django_select2.forms import Select2Widget
from phonenumber_field.formfields import RegionalPhoneNumberWidget
from .models import *
from django.core.exceptions import ValidationError
import json

class JobForm(forms.ModelForm):
    class Meta:
        model = JobDetail
        fields = '__all__'

        widgets = {
            'sender' : Select2Widget(attrs={'class': 'form-control'}),
            'client' : Select2Widget(attrs={'class': 'form-control'}),
            'jenisPekerjaan' : Select2Widget(attrs={'class': 'form-control'}),
            'kategoriPekerjaan' : forms.TextInput(attrs={'class': 'form-control'}),
            'jenisLayanan' : forms.TextInput(attrs={'class': 'form-control'}),
            'action' : forms.TextInput(attrs={'class':'form-control'}),
            'keterangan' : forms.TextInput(attrs={'class':'form-control'}),
            'status' : forms.TextInput(attrs={'class':'form-control'}),
            'gps' : forms.TextInput(attrs={'class':'form-control'}),
            'ssid' : forms.TextInput(attrs={'class':'form-control'}),
            'signal' : forms.TextInput(attrs={'class':'form-control'}),
            'freq' : forms.TextInput(attrs={'class':'form-control'}),
            'perangkatInstall' : forms.TextInput(attrs={'class':'form-control'}),
            'perangkatDismantle' : forms.TextInput(attrs={'class':'form-control'}),
            'pelaksanaPekerjaan' : forms.SelectMultiple(attrs={'class': 'form-control', 'multiple': 'true'}),
            'jamMulai' : forms.TimeInput(attrs={'type': 'time', 'class':'form-control'}),
            'jamSelesai' : forms.TimeInput(attrs={'type': 'time', 'class':'form-control'}),
            'tanggal': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'tanggal' : 'Tanggal Pelaksanaan',
            'jenisPekerjaan' : 'Jenis Pekerjaan',
            'kategoriPekerjaan' : 'Kategori Pekerjaan',
            'jenisLayanan' : 'Jenis Layanan',
            'gps' : 'GPS',
            'ssid' : 'SSID',
            'perangkatInstall' : 'Perangkat Install',
            'perangkatDismantle' : 'Perangkat Dismantle',
            'pelaksanaPekerjaan' : 'Pelaksana Pekerjaan',
            'jamMulai' : 'Jam Mulai',
            'jamSelesai' : 'Jam Selesai',
        }
    timestamp = forms.DateTimeField(
        widget=widgets.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'placeholder': 'Timestamp'}),
        label='Timestamp',
        required=False
    )

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'namaPelanggan' : forms.TextInput(attrs={'class' : 'form-control'}),
            'nomorTelponPelanggan' : RegionalPhoneNumberWidget(region='ID', attrs={'class': 'form-control', 'placeholder': '081-234-567-890'}),
        }
    
class ClientPICForm(forms.ModelForm):
    class Meta:
        model = ClientPIC
        fields = '__all__'
        exclude = ['client_id']
        widgets = {
            'namaPIC' : forms.TextInput(attrs={'class':'form-control'}),
            'nomorTelponPIC' : RegionalPhoneNumberWidget(region='ID', attrs={'class': 'form-control', 'placeholder': '081-234-567-890'}),
        }
        labels = {
            'namaPIC': 'Nama PIC',
            'nomorTelponPIC': 'No Telpon PIC',
        }

class ClientAlamatForm(forms.ModelForm):
    class Meta:
        model = ClientAlamat
        fields = '__all__'
        widgets = {
            'client' : Select2Widget(attrs={'class' : 'form-control'}),
            'provinsi': Select2Widget(attrs={'class': 'form-control'}),
            'kota': Select2Widget(attrs={'class': 'form-control'}),
            'kecamatan': Select2Widget(attrs={'class': 'form-control'}),
            'kelurahan': Select2Widget(attrs={'class': 'form-control'}),
            'kode_pos': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Kode Pos'}),
            'detail': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ruko, Jl. Permata Regency Jl. H. Kelik No.31 Blok C, RT.1/RW.6,'}),
        }
        labels = {
            'provinsi': 'Provinsi',
            'kota': 'Kota',
            'kecamatan': 'Kecamatan',
            'kelurahan': 'Kelurahan',
            'kode_pos': 'Kode Pos',
            'detail': 'Alamat Detail',
        }

class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = '__all__'
        widgets = {
            'nama' : forms.TextInput(attrs={'class': 'form-control'}),
            'ktp' : forms.NumberInput(attrs={'class': 'form-control'}),
            'telponWorker' : RegionalPhoneNumberWidget(region='ID', attrs={'class': 'form-control', 'placeholder': '081-234-567-890'}),
            'rekening' : forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nama': 'Nama Worker',
            'ktp': 'No KTP',
            'telponWorker': 'No Telpon',
            'rekening': 'No Rekening',
        }