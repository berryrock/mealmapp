from django.urls import path
from . import views

urlpatterns = [
	path('', views.main_page, name='main_page'),
	path('about/', views.about_page, name='about_page'),
	path('app/', views.app_page, name='app_page'),
	path('news/', views.news_list, name='news_list'),
	path('news/<slug:url>/', views.news_detail, name='news_detail'),
	path('blog/', views.post_list, name='post_list'),
	path('blog/<slug:url>/', views.post_detail, name='post_detail'),
]