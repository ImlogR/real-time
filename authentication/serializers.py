
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name','password', 'password2']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs

    def create(self, validated_data):
        email = validated_data.get("email")
        first_name = validated_data.get("first_name")

        user= CustomUser.objects.create(email= email, first_name= first_name)
        user.set_password(validated_data['password'])
        user.save()
        return user