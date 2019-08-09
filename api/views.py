from rest_framework import generics, permissions
from api.models import AppUser, MealHistory, Dish, Product, Region, RegionVector
from api.serializers import MealHistorySerializer, UserSerializer, DishSerializer, RegionVectorSerializer
from api.permissions import IsOwnerOrReadOnly

class MealList(generics.ListCreateAPIView):
	"""
	List all meals, or create a new meal.
	"""
	permission_classes = (permissions.IsAuthenticated,)
	queryset = MealHistory.objects.get_queryset().order_by('-pk')
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
	queryset = AppUser.objects.get_queryset().order_by('id')
	serializer_class = UserSerializer

class UserDetailed(generics.RetrieveUpdateAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	queryset = AppUser.objects.all()
	serializer_class = UserSerializer

#class UserVector(generics.RetrieveAPIView):
#	permission_classes = (permissions.IsAuthenticated,)
#	queryset = AppUser.objects.all()
#	serializer_class = UserVectorSerializer	

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
