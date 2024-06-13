# Standard library imports
import os
import json
import uuid
from datetime import datetime, timedelta, timezone

# Third-party imports
from itertools import groupby
from operator import itemgetter
from PIL import Image, ImageFile
from collections import defaultdict
from django.urls import reverse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, permission_classes

# Local application imports
from .forms import *
from .models import *
from .serializers import *
from page1.models import Provinsi, Kota, Kecamatan, Kelurahan, KodePos

# Django imports
from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from django.db.models import Count, Sum
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models.functions import ExtractDay, ExtractMonth, ExtractYear, Upper

# Create your views here.
# -------------------- Common Functions --------------------#
def delete_selected_rows(request, model, key):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids[]')  # Assuming you're sending an array of selected IDs
        try:
            selected_items = model.objects.filter(**{f'{key}__in': selected_ids})

            # Additional logic for image deletion if applicable
            if hasattr(model, 'lampiran') and hasattr(model, 'lampiran_og'):
                for item in selected_items:
                    image_path = os.path.join(settings.MEDIA_ROOT, str(item.lampiran))
                    og_image_path = os.path.join(settings.MEDIA_ROOT, str(item.lampiran_og))
                    if os.path.exists(image_path) and os.path.exists(og_image_path):
                        os.remove(image_path)
                        os.remove(og_image_path)
                    else:
                        print(f"Image file not found:\nResized Image: {image_path}\nOriginal Image: {og_image_path}")
                    

            selected_items.delete()  # Delete the selected rows from the database
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

def add_entity_view(request, entity_form, template_name, redirect_template, initial = None):
    entity_form_instance = entity_form(request.POST or None)
    if request.method == 'POST':
        form = entity_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect(redirect_template)
    else:
        print(initial)
        if (initial):
            form = (entity_form(initial=initial))
            entity_form_instance = form
        else: 
            form = entity_form()

    return render(request, template_name, {'entity_form': entity_form_instance})

def add_entity(request, entity_id, entity_model, form_class, template_name, entity_field, entity_form_field, initial_data=None, redirect_url = None):
    entity = get_object_or_404(entity_model, **{entity_field: entity_id})

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            setattr(form.instance, entity_form_field, entity)
            form.save()
            if redirect_url:
                return redirect(redirect_url)
    else:
        form = form_class(initial=initial_data)

    return render(request, template_name, {'entity': entity, 'form': form, 'entity_id': entity_id})

@login_required
def display_entities(request, entity_model, template_name):
    entities = entity_model.objects.all()
    return render(request, template_name, {'entities': entities})

def entity_detail(request, entity_model, entity_form, entity_id_field, entity_id, template_name, extra_context=None):
    entity = get_object_or_404(entity_model, **{entity_id_field: entity_id})
    form = entity_form(instance=entity)
    context = {'entity': entity, 'form': form, 'entity_id': entity_id}

    if extra_context:
        context.update(extra_context)

    return render(request, template_name, context)

def delete_entity(request, entity_model, entity_id_field, entity_id):
    entity = get_object_or_404(entity_model, **{entity_id_field: entity_id})

    if request.method == 'POST':
        # Additional logic for image deletion if applicable
        if hasattr(entity, 'lampiran') and hasattr(entity, 'lampiran_og'):
            image_path = os.path.join(settings.MEDIA_ROOT, str(entity.lampiran))
            og_image_path = os.path.join(settings.MEDIA_ROOT, str(entity.lampiran_og))
            if os.path.exists(image_path):
                os.remove(image_path)
            else:
                print(f"Image file not found: {image_path}")
                
            if os.path.exists(og_image_path):
                os.remove(og_image_path)
            else:
                print(f"Original image file not found: {og_image_path}")

        entity.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def edit_entity(request, entity_model, entity_form, entity_id_field, entity_id):
    entity = get_object_or_404(entity_model, **{entity_id_field: entity_id})

    if request.method == 'POST':
        form = entity_form(request.POST, instance=entity)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = entity_form(instance=entity)

    return render(request, 'edit_entity.html', {'form': form})

@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password') 
    user = authenticate(username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        groups = list(user.groups.values_list('id', flat=True))
        serializedUser = UserSerializer(user)
        print(groups)
        return Response({'token': token.key, 'groups': groups, 'user' : serializedUser.data}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)  

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)

class add_client_mobile(generics.CreateAPIView):
    serializer_class = ClientSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            client = serializer.save()
            return Response({'client_id': client.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class add_client_PIC_mobile(generics.CreateAPIView):
    serializer_class = ClientPICSerializer

    def post(self, request, client_id, *args, **kwargs):
        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data.copy()
        data['client'] = client.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class add_client_address_mobile(generics.CreateAPIView):
    serializer_class = ClientAlamatSerializer

    def post(self, request, client_id, *args, **kwargs):
        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data.copy()
        data['client'] = client.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class add_job_mobile(generics.CreateAPIView):
    serializer_class = JobDetailSerializer
    parser_classes = (MultiPartParser, FormParser)
    def get_client(self, client_id):
        try:
            return Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return None
            
    def perform_create(self, serializer):
        client_id = self.kwargs['client_id']
        client = Client.objects.get(pk=client_id)
        if not client:
            raise serializers.ValidationError({'client_id': 'Client not found'})
        # If the client exists, assign its ID to the serializer's validated data
        serializer.validated_data['client'] = client

        # Ensure pelaksanaPekerjaan is passed as a list
        pelaksana_pekerjaan = self.request.data.getlist('pelaksanaPekerjaan')
        serializer.validated_data['pelaksanaPekerjaan'] = pelaksana_pekerjaan

        # Handle file uploads
        lampiran = self.request.FILES.get('lampiran')
        if lampiran:
            try:
                # Open the image using PIL
                image = Image.open(lampiran)
                image_name = str(lampiran)
                
                lampiran_og = image.resize((500, 500), Image.Resampling.LANCZOS)
                upload_date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                lampiran_og_name = f'original-{upload_date}-{image_name}'
                lampiran_og_path = os.path.join(settings.MEDIA_ROOT, 'fiber_photos', lampiran_og_name)
                
                lampiran_og.save(lampiran_og_path, optimize=True, quality=95)

                lampiran = image.resize((100, 100))  # Change the dimensions as needed
                lampiran_name = f'resized-{upload_date}-{image_name}'
                lampiran_path = os.path.join(settings.MEDIA_ROOT, 'fiber_photos', lampiran_name)
                lampiran.save(lampiran_path)
                
                serializer.validated_data['lampiran_og'] = os.path.join('fiber_photos', lampiran_og_name)
                serializer.validated_data['lampiran'] = os.path.join('fiber_photos', lampiran_name)
            except Exception as e:
                # Handle the error (e.g., log it, return a custom response)
                # For now, re-raise the exception to see it in the console
                raise e

        # Call the serializer's save method to create the Report instance
        serializer.save()

    def post(self, request, client_id, *args, **kwargs):
        client = self.get_client(client_id)
        if not client:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        
        return super().post(request, *args, **kwargs)

@api_view(['GET'])
def fetch_client_list(request):
    clients = Client.objects.all()
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)

class ClientListAPIView(generics.ListAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

class add_worker_mobile(generics.CreateAPIView):
    serializer_class = WorkerSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            worker = serializer.save()
            return Response({'worker_id': worker.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def fetch_worker_list(request):
    workers = Worker.objects.all()
    serializer = WorkerSerializer(workers, many=True)
    return Response(serializer.data)

class ProvinsiListView(generics.ListAPIView):
    queryset = Provinsi.objects.all()
    serializer_class = ProvinsiSerializer

class KotaListView(generics.ListAPIView):
    serializer_class = KotaSerializer

    def get_queryset(self):
        provinsi_id = self.kwargs['provinsi_id']
        return Kota.objects.filter(provinsi_id=provinsi_id)

class KecamatanListView(generics.ListAPIView):
    serializer_class = KecamatanSerializer

    def get_queryset(self):
        kota_id = self.kwargs['kota_id']
        return Kecamatan.objects.filter(kota_id=kota_id)
    
class KelurahanListView(generics.ListAPIView):
    serializer_class = KelurahanSerializer

    def get_queryset(self):
        kecamatan_id = self.kwargs['kecamatan_id']
        return Kelurahan.objects.filter(kecamatan_id=kecamatan_id)
    
class KodePosListView(generics.ListAPIView):
    serializer_class = KodePosSerializer 
  
    def get_queryset(self):
        kelurahan_id = self.kwargs['kelurahan_id']
        return KodePos.objects.filter(kelurahan_id=kelurahan_id)
      
@login_required
def display_fiber(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    start_date_str_ts = request.GET.get('start_date_ts')
    end_date_str_ts = request.GET.get('end_date_ts')

    if start_date_str_ts and end_date_str_ts:
        # Parse the date strings into naive datetime objects
        start_date_naive = datetime.strptime(start_date_str_ts, '%Y-%m-%d')
        end_date_naive = datetime.strptime(end_date_str_ts, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)
        # Make the naive datetime objects timezone-aware
        start_date = timezone.make_aware(start_date_naive, timezone.get_current_timezone())
        end_date = timezone.make_aware(end_date_naive, timezone.get_current_timezone())
        print(start_date, end_date)

        # Filter reports based on the timezone-aware datetime range
        entities = JobDetail.objects.filter(date_time__range=(start_date, end_date))
    elif start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)
        entities = JobDetail.objects.filter(tanggal__range=[start_date, end_date])
    else:
        entities = JobDetail.objects.all()

    return render(request, 'Fiber/display_fiber.html', {'entities': entities})

@login_required
def display_lampiran(request, url):
    return render(request, 'Fiber/display_lampiran.html', {'url': url})

@login_required
def fiber_detail(request, id):
    return entity_detail(request, JobDetail, JobForm, 'id', id, 'Fiber/fiber_detail.html')

@login_required
def edit_job(request, id):
    entity = get_object_or_404(JobDetail,id = id)
    
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES, instance=entity)
        
        if form.is_valid():
            foto = request.FILES.get('lampiran')
            og_foto = request.FILES.get('lampiran_og')

            if foto:
                resized_foto_path = process_image(foto, False)
                form.instance.lampiran = resized_foto_path
            if og_foto:
                resized_og_foto_path = process_image(og_foto, True)
                form.instance.lampiran_og = resized_og_foto_path

            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = JobDetail(instance=entity)
    
    return render(request, "/Fiber/edit_job.html", {'form': form})

def process_image(image, is_original):
    upload_date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    img = Image.open(image)

    # Generate a unique identifier
    unique_id = str(uuid.uuid4())[:8]  # Use the first 8 characters of a UUID
    
    # Strip file extension from the image filename
    image_name_without_extension, extension = os.path.splitext(image.name)
    
    # Resize the image
    if is_original:
        resized_img = img.resize((500, 500))
    else:
        resized_img = img.resize((100, 100))
    
    # Construct the resized image name
    if is_original:
        resized_image_name = f"original-{upload_date}-{unique_id}-{extension}"
    else:
        resized_image_name = f"resized-{upload_date}-{unique_id}-{extension}"
    
    # Save the resized image
    resized_image_path = os.path.join(settings.MEDIA_ROOT, 'report_photos', resized_image_name)
    resized_img.save(resized_image_path)

    relative_path = os.path.relpath(resized_image_path, settings.MEDIA_ROOT )
    
    return relative_path


@login_required
def delete_selected_rows_fiber(request):
    return delete_selected_rows(request, JobDetail, 'id')

@login_required
def delete_selected_rows_client(request):
    return delete_selected_rows(request, Client, 'id')

@api_view(['GET'])
def check_token(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        try:
            user_token = Token.objects.get(user=user)
            return Response({"token": user_token.key}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"token": ""}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@login_required
def edit_fiber(request, id):
    entity = get_object_or_404(JobDetail,id = id)

    if request.method == 'POST':
        form = JobDetail(request.POST, request.FILES, instance=entity)
        
        if form.is_valid():
            # Check if a new image file is provided
            foto = request.FILES.get('lampiran')
            og_foto = request.FILES.get('lampiran_og')

            if foto:
                resized_foto_path = process_image(foto, False)
                form.instance.foto = resized_foto_path
            if og_foto:
                resized_og_foto_path = process_image(og_foto, True)
                form.instance.og_foto = resized_og_foto_path

            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = JobForm(instance=entity)
    
    return render(request, "/fiber/edit_fiber.html", {'form': form})

def process_image(image, is_original):
    upload_date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    img = Image.open(image)

    # Generate a unique identifier
    unique_id = str(uuid.uuid4())[:8]  # Use the first 8 characters of a UUID
    
    # Strip file extension from the image filename
    image_name_without_extension, extension = os.path.splitext(image.name)
    
    # Resize the image
    if is_original:
        resized_img = img.resize((500, 500))
    else:
        resized_img = img.resize((100, 100))
    
    # Construct the resized image name
    if is_original:
        resized_image_name = f"original-{upload_date}-{unique_id}-{extension}"
    else:
        resized_image_name = f"resized-{upload_date}-{unique_id}-{extension}"
    
    # Save the resized image
    resized_image_path = os.path.join(settings.MEDIA_ROOT, 'report_photos', resized_image_name)
    resized_img.save(resized_image_path)

    relative_path = os.path.relpath(resized_image_path, settings.MEDIA_ROOT )
    
    return relative_path

@login_required
def delete_fiber(request, id):
    return delete_entity(request, JobDetail, 'id', id)

@login_required
def display_fiber_client(request):
    return display_entities(request, Client, 'Client/display_client.html')

@login_required
def client_detail(request, id):
    return entity_detail(request, Client, ClientForm, 'id', id, 'Client/client_detail.html')

@login_required
def edit_client(request, id):
    return edit_entity(request, Client, ClientForm, 'id', id)

@login_required
def delete_client(request, id):
    return delete_entity(request, Client, 'id', id)

@login_required
def edit_client_pic(request, id):
    pic = get_object_or_404(ClientPIC, id=id)
    form = ClientPICForm(request.POST or None, instance=pic)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('client_detail', id=pic.client_id.pk)
    return render(request, 'Client/edit_client_pic.html', {'form': form, 'pic': pic})

@login_required
def add_client_pic(request, id):
    redirect_url  = reverse('client_detail', args=(id,))
    return add_entity(request, id, Client, ClientPICForm, 'Client_PIC/add_client_pic.html', 'id', 'id', {'id': id}, redirect_url=redirect_url)

@login_required
def delete_client_pic(request, id):
    return delete_entity(request, ClientPIC, 'id', id)