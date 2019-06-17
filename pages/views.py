from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Page, Banner
from news.models import News

def main_page(request):
	page = get_object_or_404(Page, url='main')
	banners = Banner.objects.filter(active=True).order_by('-pk')[:1]
	last_news = News.objects.filter(published_date__lte=timezone.now()).order_by('-pk')[:3]
	return render(request, 'pages/main_page.html', {'page': page, 'last_news': last_news, 'banners': banners})

def about_page(request):
	page = get_object_or_404(Page, url='about')
	return render(request, 'pages/about.html', {'page': page})