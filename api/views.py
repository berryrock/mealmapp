from django.http import Http404
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from api.models import AppUser, MealHistory, Dish, Product, Region, RegionVector
from api.serializers import MealHistorySerializer, UserSerializer, UserVectorSerializer, UserDishInfoSerializer, DishSerializer, RegionVectorSerializer
from api.permissions import IsOwnerOrReadOnly

class MealList(generics.ListCreateAPIView):
	"""
	List all meals, or create a new meal.
	"""
	permission_classes = (permissions.IsAuthenticated,)
	queryset = MealHistory.objects.get_queryset().order_by('-pk')
	serializer_class = MealHistorySerializer

	def perform_create(self, serializer):
		app_user = AppUser.objects.get(user=self.request.user)
		print(app_user)
		serializer.save(user=app_user)

class MealDetailed(generics.RetrieveUpdateDestroyAPIView):
	"""
	Retrieve, update or delete a meal.
	"""
	permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly)
	queryset = MealHistory.objects.all()
	serializer_class = MealHistorySerializer

class UserList(generics.ListCreateAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	queryset = AppUser.objects.get_queryset().order_by('id')
	serializer_class = UserSerializer

class UserDetailed(generics.RetrieveUpdateAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	queryset = AppUser.objects.all()
	serializer_class = UserSerializer

class UserVector(APIView):
	def get_object(self, token):
		user = User.objects.get(auth_token=token)
		user_id = user.id
		try:
			return AppUser.objects.get(pk=user_id)
		except AppUser.DoesNotExist:
			raise Http404

	def get(self, request, token, format=None):
		user = self.get_object(token)
		vector = user.get_vector()
		serializer = UserVectorSerializer(vector)
		return Response(serializer.data)

class UserDishInfo(APIView):
	def get_object(self, dish):
		try:
			name = dish["dish_name"]
			return Dish.objects.get(name=name)
		except Dish.DoesNotExist:
			Dish.objects.create(name=name)
			raise Http404

	def get_user(self, user):
		user = User.objects.get(login=user)
		user_id = user.id
		try:
			return AppUser.objects.get(pk=user_id)
		except AppUser.DoesNotExist:
			raise Http404

	def post(self, request, format=None):
		dish_info = {}
		user = request.user
		dish = self.get_object(request.data)
		dish_cousine = dish.cousine
		app_user = AppUser.objects.get(pk=user.id)
		dish_desc = app_user.get_dish_info(dish.name, app_user)
		dish_info = {"user": user.id, "dish_name": dish.name, "dish_cousine": dish_cousine, "dish_desc": dish_desc}
		serializer = UserDishInfoSerializer(dish_info)
		return Response(serializer.data)

class DishList(generics.ListCreateAPIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	queryset = Dish.objects.get_queryset().order_by('id')
	serializer_class = DishSerializer

class DishDetailed(generics.RetrieveUpdateAPIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	queryset = Dish.objects.all()
	serializer_class = DishSerializer

class RegionVectorList(generics.ListAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	regionNumber = Region.objects.count()
	queryset = RegionVector.objects.get_queryset().order_by('-pk')[:regionNumber]
	serializer_class = RegionVectorSerializer
