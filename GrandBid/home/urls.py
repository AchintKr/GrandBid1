from django.contrib import admin
from django.urls import path
from home import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('test/', views.test_api),
    path('submit/', views.receive_data), 
    path('api/login_organiser/', views.login_organiser),
    path('api/register_organiser/', views.register_organiser),

]
if settings.DEBUG:
   urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)