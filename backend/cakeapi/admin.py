from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ['cakeid' ,'cakename' ]
admin.site.register(AddOrder)
admin.site.register(Carts)
admin.site.register(Checkout)
admin.site.register(CheckoutFinal)