from rest_framework import serializers
from account.models import User
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11, required=True)
    email = serializers.EmailField(max_length=50, required=True)
    password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    password2 = serializers.CharField(required=True, write_only=True)

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError('This phone_number is already exists!')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email is already exists!')
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('The two password fields don’t match')
        return super().validate(data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
