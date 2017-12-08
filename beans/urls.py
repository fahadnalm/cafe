from django.urls import path
from . import views

app_name= 'beans'

urlpatterns = [

	path('signup/', views.usersignup, name='signup'),
	path('login/', views.userlogin, name='login'),
	path('logout/', views.userlogout, name='logout'),
	path('create/', views.create_coffee, name='create'),

]