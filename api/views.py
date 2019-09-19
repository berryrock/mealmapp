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
		serializer.save(user=app_user)

class MealDetailed(generics.RetrieveUpdateDestroyAPIView):
	"""
	Retrieve, update or delete a meal.
	"""
	permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly)
	queryset = MealHistory.objects.all()
	serializer_class = MealHistorySerializer

class UserList(generics.ListCreateAPIView):
	permission_classes = (permissions.IsAuthenticated)
	queryset = AppUser.objects.get_queryset().order_by('id')
	serializer_class = UserSerializer

class UserCreation(APIView):
	def post(self, request, format=None):
		data = request.data
		email = data['email']
		username = email[:email.find("@")]
		user = User.objects.create_user(username=username,email=email,password=data['password'])
		app_user = AppUser.objects.get(user=user)
		serializer = UserSerializer(app_user)
		return Response(serializer.data)

class UserDetailed(APIView):
	permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly)
	
	def get_object(self, user_id):
		try:
			return AppUser.objects.get(pk=user_id)
		except AppUser.DoesNotExist:
			raise Http404

	def get(self, request, format=None):
		user = request.user
		app_user = self.get_object(user.id)
		serializer = UserSerializer(app_user)
		return Response(serializer.data)

	def put(self, request, format=None):
		user = request.user
		app_user = self.get_object(user.id)
		serializer = UserSerializer(app_user, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, format=None):
		user = request.user
		app_user = self.get_object(user.id)
		user.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class UserVector(APIView):
	def get(self, request, format=None):
		user = request.user
		app_user = AppUser.objects.get(pk=user.id)
		vector = app_user.get_vector()
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
