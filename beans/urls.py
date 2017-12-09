from django.urls import path
from . import views

app_name= 'beans'

urlpatterns = [

	path('signup/', views.usersignup, name='signup'),
	path('login/', views.userlogin, name='login'),
	path('logout/', views.userlogout, name='logout'),
	path('create/', views.create_coffee, name='create'),
	path('ajax_price/', views.ajax_price, name="ajax_price"),
	path('coffee_list/', views.coffee_list, name='coffee_list'),
	path('coffee_detail/<int:coffee_detail>', views.coffee_detail, name="coffee_detail"),

]