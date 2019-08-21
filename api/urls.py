from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
	path('mealhistory/', views.MealList.as_view()),
	path('mealhistory/<int:pk>/', views.MealDetailed.as_view()),
	path('users/', views.UserList.as_view()),
	path('users/<int:pk>/', views.UserDetailed.as_view()),
	path('users/<slug:token>/preferencevector/', views.UserVector.as_view()),
	path('users/dish_info/', views.UserDishInfo.as_view()),
	path('dishes/', views.DishList.as_view()),
	path('dishes/<int:pk>/', views.DishDetailed.as_view()),
	path('vector/', views.RegionVectorList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)