from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.utils import timezone
from .models import Post
from map.models import User, Dish, Product, MealHistory

def post_list(request):
	users = User.objects.count()
	dishes = Dish.objects.count()
	products = Product.objects.count()
	meals = MealHistory.objects.filter(date_time__lte=timezone.now()+timezone.timedelta(days=1)).count()
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/blog_list.html', {'posts': posts, 'users': users, 'meals': meals, 'dishes': dishes, 'products': products})

def post_detail(request, url):
	post = get_object_or_404(Post, url=url)
	return render(request, 'blog/blog_detail.html', {'post': post})