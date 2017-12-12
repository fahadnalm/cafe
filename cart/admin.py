from django.contrib import admin
from .models import Cart, CartItem, City, UserAddress, Order

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(City)
admin.site.register(UserAddress)
admin.site.register(Order)


