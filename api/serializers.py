from rest_framework import serializers
from api.models import AppUser, MealHistory, Dish, Product

class MealHistorySerializer(serializers.ModelSerializer):
	user = serializers.ReadOnlyField(source='user.id')

	class Meta:
		model = MealHistory
		fields = ('id', 'date_time', 'user', 'dish', 'point', 'location', 'weight', 'acne', 'accepted')

class UserSerializer(serializers.ModelSerializer):
	meals = serializers.PrimaryKeyRelatedField(many=True,queryset=MealHistory.objects.all())

	class Meta:
		model = AppUser
		fields = ('id', 'name', 'surname', 'email', 'phone', 'telegram', 'registration', 'birthday', 'length', 'meals')

class DishSerializer(serializers.ModelSerializer):
	#dishes = serializers.PrimaryKeyRelatedField(many=True,queryset=Dish.objects.all())

	class Meta:
		model = Dish
		fields = ('id', 'name', 'cousine', 'TYPE', 'products', 'comments', 'avg_point')


'''
    def create(self, validated_data):
        """
        Create and return a new `meal` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `meal` instance, given the validated data.
        """
        instance.date_time = validated_data.get('date_time', instance.date_time)
        instance.user = validated_data.get('user', instance.user)
        instance.dish = validated_data.get('dish', instance.dish)
        instance.point = validated_data.get('point', instance.point)
        instance.location = validated_data.get('location', instance.location)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.acne = validated_data.get('acne', instance.acne)
        instance.accepted = validated_data.get('accepted', instance.accepted)
        instance.save()
        return instance
'''