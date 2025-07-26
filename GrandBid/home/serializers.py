from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Organiser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class OrganiserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Organiser
        fields = ['user', 'phone_number', 'organization_name']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        organiser = Organiser.objects.create(user=user, **validated_data)
        return organiser
