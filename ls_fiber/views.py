# Standard library imports
import os
import json
import uuid
from datetime import datetime, timedelta

# Third-party imports
from itertools import groupby
from operator import itemgetter
from PIL import Image, ImageFile
from collections import defaultdict
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
            if hasattr(model, 'foto') and hasattr(model, 'og_foto'):
                for item in selected_items:
                    image_path = os.path.join(settings.MEDIA_ROOT, str(item.foto))
                    og_image_path = os.path.join(settings.MEDIA_ROOT, str(item.og_foto))
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


class get_worker(generics.ListAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

    def get_queryset(self):
        return Worker.objects.all()
