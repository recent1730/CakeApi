from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db.models import Q
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator
from .models import *
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode



from django.contrib.auth.models import User

class CakeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cake
        fields = '__all__'


class AllCakeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cake
        fields = ['cakeid' , 'image' , 'name' , 'price']

#
class AddtocartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Carts
        fields = '__all__'
#         # fields = ['cakeid', 'email', 'name', 'price' , 'image' ,'weight']
class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model =Checkout
        fields = '__all__'




















class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
        

class PlaceOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckoutFinal
        fields  = '__all__'

        def to_representation(self, instance):
            data = super().to_representation(instance)
            data['cakes'] = AddtocartSerializers(Carts.objects.filter(id__in=data['cakes']), many=True).data
            return data























class UserSerializers(serializers.ModelSerializer):
    email=serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    username=serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    password=serializers.CharField(max_length=8)

    def create(self, validated_data):
        user=User.objects.create_user(validated_data['username'],validated_data['email'],validated_data['password'])
        return user
    class Meta:
        model=User
        fields=['id','username','email','password']

        def __str__(self):
            return self.first_name



class UserLoginSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        required=False,
        allow_blank=True,
        write_only=True,
    )

    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        write_only=True,
        label="Email Address"
    )

    token = serializers.CharField(
        allow_blank=True,
        read_only=True
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta(object):
        model = User
        fields = ['email', 'username', 'password', 'token']

    def validate(self, data):
        email = data.get('email', None)
        username = data.get('username', None)
        password = data.get('password', None)

        if not email and not username:
            raise serializers.ValidationError("Please enter username or email to login.")

        user = User.objects.filter(
            Q(email=email) | Q(username=username)
        ).exclude(
            email__isnull=True
        ).exclude(
            email__iexact=''
        ).distinct()

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise serializers.ValidationError("This username/email is not valid.")

        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError("Invalid credentials.")

        if user_obj.is_active:
            token, created = Token.objects.get_or_create(user=user_obj)
            data['token'] = token
        else:
            raise serializers.ValidationError("User not active.")

        return data

#
# class ResetPasswordEmailRequestSerializer(serializers.Serializer):
#     email = serializers.EmailField(min_length=2)
#
#     redirect_url = serializers.CharField(max_length=500, required=False)
#
#     class Meta:
#         fields = ['email']


