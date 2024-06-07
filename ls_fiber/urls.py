from django.urls import path
from .views import *

urlpatterns = [
    path('login_user/', login_user, name="login_user"),
    path('logout_user/', logout_user, name="logout_user"),
    path('add_client_mobile/', add_client_mobile.as_view(), name="add_client_mobile"),
    path('add_job_mobile/<int:client_id>/', add_job_mobile.as_view(), name="add_job_mobile"),
    path('add_client_PIC_mobile/<int:client_id>/', add_client_PIC_mobile.as_view(), name="add_client_PIC_mobile"),
    path('add_client_address_mobile/<int:client_id>/', add_client_address_mobile.as_view(), name="add_client_address_mobile"),
]

