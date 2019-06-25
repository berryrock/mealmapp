from rest_framework import generics, permissions
from api.models import AppUser, MealHistory, Dish, Product
from api.serializers import MealHistorySerializer, UserSerializer, DishSerializer
from api.permissions import IsOwnerOrReadOnly


class MealList(generics.ListCreateAPIView):
	"""
	List all meals, or create a new meal.
	"""
	permission_classes = (permissions.IsAuthenticated,)
	queryset = MealHistory.objects.all()
	serializer_class = MealHistorySerializer

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

class MealDetailed(generics.RetrieveUpdateDestroyAPIView):
	"""
	Retrieve, update or delete a meal.
	"""
	permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly)
	queryset = MealHistory.objects.all()
	serializer_class = MealHistorySerializer

class UserList(generics.ListCreateAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	queryset = AppUser.objects.all()
	serializer_class = UserSerializer

class UserDetailed(generics.RetrieveUpdateAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	queryset = AppUser.objects.all()
	serializer_class = UserSerializer

class DishList(generics.ListCreateAPIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	queryset = Dish.objects.all()
	serializer_class = DishSerializer

class DishDetailed(generics.RetrieveUpdateAPIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	queryset = Dish.objects.all()
	serializer_class = DishSerializer