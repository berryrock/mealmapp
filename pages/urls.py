from django.urls import path
from . import views

urlpatterns = [
	path('', views.main_page, name='main_page'),
	path('', views.about_page, name='about_page'),
]