from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

from django.conf.urls import url
from rest_framework.routers import DefaultRouter
#
# from .views import AuthViewSet
#
# default_router = DefaultRouter(trailing_slash=False)
# default_router.register('auth', AuthViewSet, basename='auth')
# urlpatterns = default_router.urls
# #
from .views import CakeCartView

urlpatterns =[

    path('allcakes/', views.CakeListView.as_view(), name='cake_list'),

    path('addcake/', views.CakeAddView.as_view(), name='cake_add'),
    url('register', views.UserRegister.as_view(), name='UserRegister'),
    path('cake/<int:pk>/', views.CakeRetrieveView.as_view(), name='cake_retrieve'),
    path('search/', views.SearchAPIView.as_view()),

    url('login',views.UserLoginAPIView.as_view(),name='login'),
    path('addcaketocart/', views.AddtocartView.as_view(), name='cake_add'),
    url(r'^cakecart/', CakeCartView.as_view()),
    path('myorders/', views.myorders.as_view()),

    url(r'^removecakefromcart/', views.RemoveCakeFromCartView.as_view()),
    url(r'^placeorder/', views.placeorder.as_view()),
    url(r'^checkout/', views.CheckOut.as_view()),

    url(r'^myorder/', views.MyOrder.as_view()),
    
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    url(r'^sendmail/', views.sendmail),
   
]
   
# python manage migrate --fake cakeapi 0006_auto_20210426_1157