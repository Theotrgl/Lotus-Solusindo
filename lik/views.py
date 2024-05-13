from datetime import datetime, timedelta
from io import BytesIO
import os
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser

from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction


from PIL import Image, ImageFile

from .serializers import *
from .models import *
from .forms import *

# Create your views here.
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

@login_required
def display_report(request):
    entities = Report.objects.all()
    return render(request, 'Report/display_report.html', {'entities': entities})

@login_required
def delete_selected_rows_report(request):
    return delete_selected_rows(request, Report, 'id')

@login_required
def add_report(request, initial=None):
    entity_form_instance = ReportForm(request.POST or None)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect(redirect_template)
    else:
        print(initial)
        if (initial):
            form = (ReportForm(initial=initial))
            entity_form_instance = form
        else: 
            form = ReportForm()

    return render(request, 'Report/add_report.html', {'entity_form': entity_form_instance})

@login_required
def report_detail(request, id):
    return entity_detail(request, Report, ReportForm, 'id', id, 'Report/report_detail.html')

@login_required
def delete_report(request, id):
    return delete_entity(request, Report, 'id', id)

@login_required
def edit_report(request, id):
    return edit_entity(request, Report, ReportForm, 'id', id)

# Set maximum image quality
ImageFile.MAXBLOCK = 2**20
class add_report_mobile(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        # Get the image data from request.FILES
        image_data = self.request.FILES.get('foto')
        print(image_data)
        if image_data:
            # Open the image using PIL
            image = Image.open(image_data)
            image_name = str(image_data)
            
            og_image = image.resize((500, 500), Image.Resampling.LANCZOS)
            upload_date = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            og_image_name = f'original-{upload_date}-{image_name}'
            og_image_path = os.path.join(settings.MEDIA_ROOT,'report_photos', og_image_name)
            
            og_image.save(og_image_path, optimize = True, quality= 95)
            # image.save(og_image_path)

            resized_image = image.resize((100, 100))  # Change the dimensions as needed
            resized_image_name = f'resized-{upload_date}-{image_name}'
            resized_image_path = os.path.join(settings.MEDIA_ROOT, 'report_photos', resized_image_name)
            resized_image.save(resized_image_path)
            
            # Delete the original image file
            # os.remove(os.path.join(settings.MEDIA_ROOT, 'report_photos', image_name))
            serializer.validated_data['og_foto'] = os.path.join('report_photos', og_image_name)
            serializer.validated_data['foto'] = os.path.join('report_photos', resized_image_name)
        # Call the serializer's save method to create the Report instance
        serializer.save()

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


# @permission_classes([IsAuthenticated])
class GroupLokasiListAPIView(generics.ListAPIView):
    serializer_class = LokasiSerializer

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        group_lokasis = Group_Lokasi.objects.filter(group_id=group_id)
        lokasi_ids = [lokasi.id for group_lokasi in group_lokasis for lokasi in group_lokasi.lokasi.all()]
        return Lokasi.objects.filter(id__in=lokasi_ids)
    
# @permission_classes([IsAuthenticated])
class GroupTujuanListAPIView(generics.ListAPIView):
    serializer_class = TujuanSerializer

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        group_tujuans = Group_Tujuan.objects.filter(group_id=group_id)
        tujuan_ids = [tujuan.id for group_tujuan in group_tujuans for tujuan in group_tujuan.tujuan.all()]
        return Tujuan.objects.filter(id__in=tujuan_ids)

# @permission_classes([IsAuthenticated])
class GroupKayuListAPIView(generics.ListAPIView):
    serializer_class = KayuSerializer

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        group_kayus = Group_Kayu.objects.filter(group_id=group_id)
        kayu_ids = [kayu.id for group_kayu in group_kayus for kayu in group_kayu.kayu.all()]
        return Kayu.objects.filter(id__in=kayu_ids)

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
def display_group(request):
    group_lokasi = Group_Lokasi.objects.all()
    group_tujuan = Group_Tujuan.objects.all()
    group_kayu = Group_Kayu.objects.all()

    group_data = {}

    for gl in group_lokasi:
        group_id = gl.group.id
        group_data.setdefault(group_id, {'group': gl.group, 'lokasi': set(), 'tujuan': set(), 'kayu': set()})
        group_data[group_id]['lokasi'] |= set(gl.lokasi.all())

    for gt in group_tujuan:
        group_id = gt.group.id
        group_data.setdefault(group_id, {'group': gt.group, 'lokasi': set(), 'tujuan': set(), 'kayu': set()})
        group_data[group_id]['tujuan'] |= set(gt.tujuan.all())

    for gk in group_kayu:
        group_id = gk.group.id
        group_data.setdefault(group_id, {'group': gk.group, 'lokasi': set(), 'tujuan': set(), 'kayu': set()})
        group_data[group_id]['kayu'] |= set(gk.kayu.all())

    group_data_list = list(group_data.values())

    # Retrieve all Kayu, Lokasi, and Tujuan objects
    all_kayu = Kayu.objects.all()
    all_lokasi = Lokasi.objects.all()
    all_tujuan = Tujuan.objects.all()

    return render(request, 'Group/display_groups.html', {'group_data': group_data_list, 'all_kayu': all_kayu, 'all_lokasi': all_lokasi, 'all_tujuan': all_tujuan})

@login_required
@transaction.atomic
def save_group_changes(request):
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        kayu_ids = request.POST.getlist('kayu_ids[]')
        lokasi_ids = request.POST.getlist('lokasi_ids[]')
        tujuan_ids = request.POST.getlist('tujuan_ids[]')

        try:
            # Retrieve the group object using name
            group = Group.objects.get(name=group_id)

            # Delete existing object
            Group_Kayu.objects.filter(group=group).delete()
            Group_Tujuan.objects.filter(group=group).delete()
            Group_Lokasi.objects.filter(group=group).delete()

            # Create a single Group_Kayu instance and add all kayu_ids to it
            group_kayu_instance = Group_Kayu.objects.create(group=group)
            group_kayu_instance.kayu.add(*kayu_ids)

            # Similar process for Group_Lokasi and Group_Tujuan
            group_lokasi_instance = Group_Lokasi.objects.create(group=group)
            group_lokasi_instance.lokasi.add(*lokasi_ids)

            group_tujuan_instance = Group_Tujuan.objects.create(group=group)
            group_tujuan_instance.tujuan.add(*tujuan_ids)
            
            return JsonResponse({'success': True})
        except Group.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Group not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
        
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
