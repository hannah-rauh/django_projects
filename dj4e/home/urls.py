from django.urls import path
from django.views.generic import TemplateView
from . import views

 #https://docs.djangoproject.com/en/2.1/topics/http/urls/
urlpatterns = [
    path('', TemplateView.as_view(template_name='main.html'), name='main'),
    path('hello/', TemplateView.as_view(template_name= 'hello.html'), name='hello'),
    path('funky',views.funky),
    #path('autos',dj4e/autos/urls.py),
]