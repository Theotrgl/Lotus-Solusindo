from django.contrib import admin
from .models import *
from django.utils.timezone import localtime

class JobDetailAdmin(admin.ModelAdmin):
    list_display = ('sender', 'get_local_timestamp')

    def get_local_timestamp(self, obj):
        return localtime(obj.timestamp).strftime('%Y-%m-%d %H:%M:%S %Z')

    get_local_timestamp.short_description = 'Timestamp (Local Time)'

admin.site.register(JobDetail, JobDetailAdmin)
admin.site.register(Client)
admin.site.register(ClientPIC)
admin.site.register(ClientAlamat)
admin.site.register(Worker)