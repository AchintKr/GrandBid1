from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User,auth,Group
from .models import *
from django.contrib.auth.decorators import login_required,user_passes_test
from itertools import chain
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
import  random
import datetime 
import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.core.files.storage import default_storage
from django.conf import settings
import cv2
import numpy as np
import pickle
from .helpers import *
from .serializers import *
# Create your views here.

@csrf_exempt
def test_api(request):
    return JsonResponse({'message': 'Hello from Django!'})

@api_view(['POST'])
def receive_data(request):
    name = request.data.get('name')
    email = request.data.get('email')
    
    print(f"Received: {name}, {email}")  # for debug
    return Response({"message": f"Data received for {name}"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def login_organiser(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        try:
            organiser = Organiser.objects.get(user=user)
        except Organiser.DoesNotExist:
            return Response({"error": "User is not registered as an organiser."}, status=status.HTTP_403_FORBIDDEN)

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "username": user.username,
            "organiser_id": organiser.id,
            "organization_name": organiser.organization_name,
        }, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def register_organiser(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    organization_name = request.data.get('organization_name')
    phone_number = request.data.get('phone_number')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(username=username, email=email, password=password)
        organiser = Organiser.objects.create(user=user, organization_name=organization_name, phone_number=phone_number)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'message': 'Organizer registered successfully',
            'token': token.key,
            'organiser_id': organiser.id,
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)