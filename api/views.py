from django.http import Http404
from django.db import IntegrityError
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from api.models import AppUser, MealHistory, Dish, Product, Region, RegionVector
from api.serializers import MealHistorySerializer, UserSerializer, UserVectorSerializer, UserDishInfoSerializer, DishSerializer, RegionVectorSerializer
from api.permissions import IsOwnerOrReadOnly

is_telegram = User.objects.get(username='berryrock')

class MealList(generics.ListCreateAPIView):
	"""
	List all meals, or create a new meal.
	"""
	permission_classes = (permissions.IsAuthenticated,)
	queryset = MealHistory.objects.get_queryset().order_by('-pk')
	serializer_class = MealHistorySerializer

	def get_user(self, user_id=None, telegram=None):
		try:
			if user_id:
				return AppUser.objects.get(pk=user_id)
			elif telegram:
				return AppUser.objects.get(telegram=telegram)
		except AppUser.DoesNotExist:
			raise Http404

	def perform_create(self, serializer):
		if self.request.user == is_telegram:
			user = self.request.data['telegram']
			app_user = self.get_user(telegram=user)
		else:
			user = self.request.user
			app_user = self.get_user(user_id=user.id)
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

class UserCreation(APIView):
	def post(self, request, format=None):
		data = request.data
		try:
			email = data['email']
			username = email[:email.find("@")]
			user = User.objects.create_user(username=username,email=email,password=data['password'])
			app_user = AppUser.objects.get(user=user)
			serializer = UserSerializer(app_user)
			return Response(serializer.data)
		except KeyError:
			try:
				telegram = data['telegram']
				username = telegram + '_tele'
				password = User.objects.make_random_password()
				user = User.objects.create_user(username=username,password=password)
				app_user = AppUser.objects.get(user=user)
				AppUser.objects.filter(user=user).update(telegram=telegram)
				serializer = UserSerializer(app_user)
				return Response(serializer.data)
			except IntegrityError as e:
				if 'unique constraint' in e.args[0]:
					data = {'details': 'User already exists'}
					return Response(data)
		except IntegrityError as e:
			if 'unique constraint' in e.args[0]:
				data = {'details': 'User already exists'}
				return Response(data)

class UserDetailed(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	
	def get_object(self, user_id=None, telegram=None):
		try:
			if user_id:
				return AppUser.objects.get(pk=user_id)
			elif telegram:
				return AppUser.objects.get(telegram=telegram)
		except AppUser.DoesNotExist:
			raise Http404

	def get(self, request, format=None):
		if request.user == is_telegram:
			user = request.query_params['telegram']
			app_user = self.get_object(telegram=user)
		else:
			user = request.user
			app_user = self.get_object(user_id=user.id)
		serializer = UserSerializer(app_user)
		return Response(serializer.data)

	def put(self, request, format=None):
		print(request.user)
		if request.user == is_telegram:
			user = request.data['telegram']
			app_user = self.get_object(telegram=user)
		else:
			user = request.user
			app_user = self.get_object(user_id=user.id)
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
	def get_object(self, user_id=None, telegram=None):
		try:
			if user_id:
				return AppUser.objects.get(pk=user_id)
			elif telegram:
				return AppUser.objects.get(telegram=telegram)
		except AppUser.DoesNotExist:
			raise Http404

	def get(self, request, format=None):
		if request.user == is_telegram:
			user = request.query_params['telegram']
			app_user = self.get_object(telegram=user)
		else:
			user = request.user
			app_user = self.get_object(user_id=user.id)
		vector = app_user.get_vector()
		serializer = UserVectorSerializer(vector)
		return Response(serializer.data)

class UserDishInfo(APIView):
	def get_object(self, dish):
		try:
			name = dish["dish_name"]
			return Dish.objects.get(name=dish)
		except Dish.DoesNotExist:
			Dish.objects.create(name=dish)
			raise Http404

	def get_user(self, user_id=None, telegram=None):
		try:
			if user_id:
				return AppUser.objects.get(pk=user_id)
			elif telegram:
				return AppUser.objects.get(telegram=telegram)
		except AppUser.DoesNotExist:
			raise Http404

	def post(self, request, format=None):
		dish_info = {}
		if request.user == is_telegram:
			user = request.data['telegram']
			app_user = self.get_user(telegram=user)
		else:
			user = request.user
			app_user = self.get_user(user_id=user.id)
		try:
			dish_name = request.data["dish_name"]
			dish = self.get_object(dish_name)
		except:
			raise Http404
		dish_cousine = dish.cousine
		dish_desc = app_user.get_dish_info(dish.name, app_user)
		dish_info = {"user": app_user.user.id, "dish_name": dish.name, "dish_cousine": dish_cousine, "dish_desc": dish_desc}
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
