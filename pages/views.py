from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Page, Banner, News, Post
from map.models import AppUser, Dish, Product, MealHistory

def main_page(request):
	page = get_object_or_404(Page, url='main')
	banners = Banner.objects.filter(active=True).order_by('-pk')[:1]
	last_news = News.objects.filter(published_date__lte=timezone.now()).order_by('-pk')[:3]
	return render(request, 'pages/main_page.html', {'page': page, 'last_news': last_news, 'banners': banners})

def about_page(request):
	page = get_object_or_404(Page, url='about')
	users = AppUser.objects.count()
	dishes = Dish.objects.count()
	products = Product.objects.count()
	meals = MealHistory.objects.filter(date_time__lte=timezone.now()+timezone.timedelta(days=1)).count()
	return render(request, 'pages/about.html', {'page': page, 'users': users, 'meals': meals, 'dishes': dishes, 'products': products})

def app_page(request):
	page = get_object_or_404(Page, url='app')
	return render(request, 'pages/app.html', {'page': page})

def news_list(request):
	newses = News.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'news/news_list.html', {'newses': newses})

def news_detail(request, url):
	news = get_object_or_404(News, url=url)
	return render(request, 'news/news_detail.html', {'news': news})

def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/blog_list.html', {'posts': posts})

def post_detail(request, url):
	post = get_object_or_404(Post, url=url)
	return render(request, 'blog/blog_detail.html', {'post': post})