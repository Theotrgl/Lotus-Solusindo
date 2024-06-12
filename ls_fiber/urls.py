from django.urls import path
from .views import *

urlpatterns = [
    path('login_user/', login_user, name="login_user"),
    path('logout_user/', logout_user, name="logout_user"),
    path('fetch_client_list/', fetch_client_list, name="fetch_client_list"),
    path('fetch_worker_list/', fetch_worker_list, name="fetch_worker_list"),
    path('add_client_mobile/', add_client_mobile.as_view(), name="add_client_mobile"),
    path('add_job_mobile/<int:client_id>/', add_job_mobile.as_view(), name="add_job_mobile"),
    path('add_client_PIC_mobile/<int:client_id>/', add_client_PIC_mobile.as_view(), name="add_client_PIC_mobile"),
    path('add_client_address_mobile/<int:client_id>/', add_client_address_mobile.as_view(), name="add_client_address_mobile"),
    path('add_worker_mobile/', add_worker_mobile.as_view(), name="add_worker_mobile"),

    path('provinsi/', ProvinsiListView.as_view(), name='provinsi-list'),
    path('provinsi/<int:provinsi_id>/kota/', KotaListView.as_view(), name='kota-list'),
    path('kota/<int:kota_id>/kecamatan/', KecamatanListView.as_view(), name='kecamatan-list'),
    path('kecamatan/<int:kecamatan_id>/kelurahan/', KelurahanListView.as_view(), name='kelurahan-list'),
    path('kelurahan/<int:kelurahan_id>/kodepos/', KodePosListView.as_view(), name='kodepos-list'),
]

