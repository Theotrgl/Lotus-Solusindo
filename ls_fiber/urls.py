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
    path('add_pic_client/<int:id>',add_client_pic,name='add_pic_client'),
    path('display_fiber/', display_fiber, name='display_fiber'),
    path('display_lampiran/<path:url>', display_lampiran, name="display_lampiran"),
    path('display_fiber_client/', display_fiber_client, name="display_fiber_client"),
    path('fiber_detail/<int:id>/', fiber_detail, name="fiber_detail"),
    path('client_detail/<int:id>/', client_detail, name="client_detail"),
    path('delete_selected_rows_fiber/', delete_selected_rows_fiber, name='delete_selected_rows_fiber'),
    path('delete_selected_rows_client/', delete_selected_rows_client, name='delete_selected_rows_client'),
    path('delete_fiber/<int:id>/', delete_fiber, name='delete_fiber'),
    path('delete_client/<int:id>/', delete_client, name='delete_client'),
    path('delete_client_pic/<int:pic_id>/', delete_client_pic, name='delete_client_pic'),
    path('edit_fiber/<int:id>/', edit_fiber, name='edit_fiber'),
    path('edit_client/<int:id>/', edit_client, name='edit_client'),
    path('edit_client_pic/<int:id>/', edit_client_pic, name='edit_client_pic'),
    path('check_token/<int:user_id>/', check_token, name='check_token'),
    path('provinsi/', ProvinsiListView.as_view(), name='provinsi-list'),
    path('provinsi/<int:provinsi_id>/kota/', KotaListView.as_view(), name='kota-list'),
    path('kota/<int:kota_id>/kecamatan/', KecamatanListView.as_view(), name='kecamatan-list'),
    path('kecamatan/<int:kecamatan_id>/kelurahan/', KelurahanListView.as_view(), name='kelurahan-list'),
    path('kelurahan/<int:kelurahan_id>/kodepos/', KodePosListView.as_view(), name='kodepos-list'),

]

