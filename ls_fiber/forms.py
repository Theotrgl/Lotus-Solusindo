from django import forms
from django.forms import widgets
from django_select2.forms import Select2Widget
from phonenumber_field.formfields import RegionalPhoneNumberWidget
from .models import *

class JobForm(forms.ModelForm):
     class Meta:
        model = JobDetail
        fields = '__all__'

        widgets = {
            'sender' : Select2Widget(attrs={'class': 'form-control'}),
            'client' : Select2Widget(attrs={'class': 'form-control'}),
            'tanggal': forms.DateInput(attrs={'class': 'form-control'}),
            'jenisPekerjaan' : Select2Widget(attrs={'class': 'form-control'}),
            'kategoriPelayanan' : Select2Widget(attrs={'class': 'form-control'}),
            'jenisLayanan' : Select2Widget(attrs={'class': 'form-control'}),
            'action' : forms.TextInput(attrs={'class':'form-control'}),
            'keterangan' : forms.TextInput(attrs={'class':'form-control'}),
            'gps' : forms.TextInput(attrs={'class':'form-control'}),
            'ssid' : forms.TextInput(attrs={'class':'form-control'}),
            'signal' : forms.TextInput(attrs={'class':'form-control'}),
            'freq' : forms.TextInput(attrs={'class':'form-control'}),
            'status' : forms.TextInput(attrs={'class':'form-control'}),
            'perangkatInstall' : forms.TextInput(attrs={'class':'form-control'}),
            'perangkatDismantle' : forms.TextInput(attrs={'class':'form-control'}),
            'jamMulai' : forms.TimeInput(attrs={'class':'form-control'}),
            'jamSelesai' : forms.TimeInput(attrs={'class':'form-control'}),
            'pelaksanaPekerjaan' : forms.Textarea(attrs={'class':'form-control'}),
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widget={
            'user' : Select2Widget(attrs={'class' : 'form-control'}),
            'username' : forms.TextInput(attrs={'class':'form-control'})
        }
    
class ClientPICForm(forms.ModelForm):
    class Meta:
        model = ClientPIC
        fields = '__all__'
        widget = {
            'client' : Select2Widget(attrs={'class' : 'form-control'}),
            'nama' : forms.TextInput(attrs={'class':'form-control'}),
            'telp' : RegionalPhoneNumberWidget(attrs={'class': 'form-control', 'placeholder': '081-234-567-890'}),
            'email' : forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'username@lotuslestari.co.id'})
        }

class ClientAlamatForm(forms.ModelForm):
    class Meta:
        model = ClientAlamat
        fields = '__all__'
        widget = {
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
