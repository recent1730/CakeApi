from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.urls import reverse
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, RetrieveDestroyAPIView

from rest_framework.generics import RetrieveAPIView
from rest_framework import status, generics, filters, viewsets, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import CakeSerializer, AllCakeSerializer, UserSerializers, UserLoginSerializer, AddtocartSerializers, \
    PlaceOrderSerializer, CheckoutSerializer
from  .import serializers

from rest_framework import generics, permissions, status, views
from rest_framework.authentication import TokenAuthentication
from .utils import get_and_authenticate_user, Util

class placeorder(APIView):

    def post(self,request):
        if request.method == 'POST':
            data1 =request.data
            temp =[]
            for cake in data1['cakes']:
                temp.append(cake['id'])
            print(temp)
            data1['cakes']=temp
            print(data1)

            serialize = PlaceOrderSerializer(data=data1,context={"request":request})
            if serialize.is_valid():
                serialize.save()
                queryset = Carts.objects.filter(email=request.data['email']).delete()
                # print(queryset)
                return Response({"message": "order placed","order":serialize.data},status=status.HTTP_200_OK)
            return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)

class myorders(ListAPIView):
    # permission_classes =[IsAuthenticated]
    def post(self,request):
        queryset =CheckoutFinal.objects.filter(email=request.data['email'])
        serialize = PlaceOrderSerializer(queryset,context={"request":request},many=True)
        return Response({"cakeorders":serialize.data},status=status.HTTP_200_OK)


class CakeAddView(CreateAPIView):
    serializer_class = CakeSerializer


class CakeListView(ListAPIView):
    queryset = Cake.objects.all()
    # print(queryset)
    # print(serializer.data)
    serializer_class = AllCakeSerializer


class CakeRetrieveView(RetrieveAPIView):
    queryset = Cake.objects.all()
    serializer_class = CakeSerializer


class SearchAPIView(generics.ListCreateAPIView):
    search_fields = ['name']
    filter_backends = (filters.SearchFilter,)
    queryset = Cake.objects.all()
    serializer_class = CakeSerializer


class AddtocartView(CreateAPIView):

    serializer_class = AddtocartSerializers

class CakeCartView(APIView):
    def post(self,request):
        data=request.data['email']
        print("data to be search",data)
        result=Carts.objects.filter(email=data)
        serilizer=AddtocartSerializers(result,many=True,context={'request':request})
        return Response(serilizer.data,status=status.HTTP_201_CREATED)


class RemoveCakeFromCartView(APIView):
    def post(self, request):
        email = request.data['email']
        cakeid = request.data['cakeid']
        print("email to be search", email, "cake id given", cakeid)
        result = Carts.objects.get(email=email, cakeid=cakeid)
        test = result
        if result:
            result.delete()
        serilizer = AddtocartSerializers(test)
        return Response(serilizer.data, status=status.HTTP_201_CREATED)


class CheckOut(APIView):
    def post(self,request):
        data=request.data
        serializer = CheckoutSerializer(data=data, context={'request': request})
        print("this is serialized data", serializer)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(data=serializer.data, )
        # print(serializer.errors)
        return Response(data=serializer.errors)



class PlaceOrder(APIView):
    # permission_classes=[IsAuthenticated]
    def post(self,request):
        data=request.data
        email= request.data['email']
        # cakeid = request.data['cakeid']
        print("email to be added plaxe..", email)
        result = Carts.objects.get(email=email)
        print("sahi  hai ki nahi ..... ", result)

        
        id = result.cakeid
        print(id)
        serializer = PlaceOrderSerializer(data=data ,partial=True)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            print(serializer.data['id'])
            obj = AddOrder.objects.get(id = serializer.data['id'])
            for i in id:
                print("Cake Id ..... " , i.cakeid)
                obj.Cakes.add(Carts.objects.get(cakeid=i.cakeid))
            print("saved,,,,,,,,,,,")
            return Response(serializer.data , status =status.HTTP_201_CREATED)
        return Response(serializer.errors , status =status.HTTP_400_BAD_REQUEST)


class MyOrder(APIView):
    def post(self, request):
        data = request.data
        # Email_get=data['email']
        email=request.data['email']
        print("My order email ..." ,email)
        cakes_id = Carts.objects.filter(email=email)
        print("this is cakes", cakes_id)
        # order_id=Checkout.objects.filter(email=data['email'])

        serializer = AddtocartSerializers(cakes_id, context={'request': request}, many=True)
        print("before serialized data", serializer.data)
        Data = []
        for i in serializer.data:
            print(i['cakeid'])
            j = i['cakeid']
            query1 = Carts.objects.get(cakeid=j)
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&7777")
            print(query1)
            Data.append(query1)
        print("before serialized data", Data)
        serializer1 = AddtocartSerializers(Data, context={'request': request}, many=True)
        return Response(data=serializer1.data)
#
# class OrderRetrive(APIView):
#     def post(self,request):
#         order=[]
#         data = request.data
#         orders = AddOrder.objects.filter(email=data['email'])
#         print(orders.cakes.all())
#         serializer = PlaceOrderSerializer(orders,many=True)
#         # print(serializer.data)
#         for i in serializer.data:
#             a=[]
#             for j in i['cakes']:
#                 # print(i['cakes'])
#
#                 print("jjjjjjj" ,j)
#                 c = Cake.objects.get(cakeid =j)
#                 a.append(c)
#
#             print(a)
#             serializer1 = A
#



class UserRegister(APIView):
    def post(self,request):
        data=request.data
        serilizer=UserSerializers(data=data)
        if serilizer.is_valid():
            user=serilizer.save()
            if user :
                return Response(serilizer.data,status=status.HTTP_201_CREATED)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)


def sendmail(request):
    send_mail('mail from django jasleen app','this is just for check up','jasleen0711kochar@gmail.com',['jasleen0711kochar@gmail.com'],fail_silently=False)
    return HttpResponse('Mail send ho gya h')

class UserLoginAPIView(views.APIView):
    """
    Endpoint for user login. Returns authentication token on success.
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


