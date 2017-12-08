from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cafe/', include('beans.urls', namespace='cafe')),

]
