from rest_framework import serializers
from rest_framework.response import Response
from api.models import AppUser, MealHistory, Dish, Product, RegionVector

class MealHistorySerializer(serializers.ModelSerializer):
	user = serializers.ReadOnlyField(source='user.id')

	class Meta:
		model = MealHistory
		fields = ('id', 'date_time', 'user', 'dish', 'point', 'location', 'weight', 'acne', 'accepted')

class UserSerializer(serializers.ModelSerializer):
	#meals = serializers.PrimaryKeyRelatedField(many=True,queryset=MealHistory.objects.all())

	class Meta:
		model = AppUser
		fields = ('user', 'registration', 'name', 'surname', 'email', 'phone', 'region', 'length', 'birthday', 'weigth', 'telegram')

class UserVectorSerializer(serializers.Serializer):
	id = serializers.IntegerField(read_only=True)
	vector = serializers.CharField(required=False, allow_blank=True)

class UserDishInfoSerializer(serializers.Serializer):
	user = serializers.IntegerField(read_only=True)
	dish = serializers.CharField(required=True, allow_blank=False)
	dish_cousine = serializers.CharField(read_only=True, allow_blank=True) 
	dish_desc = serializers.CharField(read_only=True, allow_blank=True) 

	def create(self, data):
		dish = Dish.objects.create(name=data)

class DishSerializer(serializers.ModelSerializer):
	#dishes = serializers.PrimaryKeyRelatedField(many=True,queryset=Dish.objects.all())

	class Meta:
		model = Dish
		fields = ('id', 'name', 'cousine', 'TYPE', 'products', 'comments', 'avg_point')

class RegionVectorSerializer(serializers.ModelSerializer):
	class Meta:
		model = RegionVector
		fields = ('id', 'date_time', 'dishes', 'region')