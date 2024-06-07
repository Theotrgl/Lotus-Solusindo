from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(JobDetail)
admin.site.register(Client)
admin.site.register(ClientPIC)
admin.site.register(ClientAlamat)