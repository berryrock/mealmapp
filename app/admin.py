from django.contrib import admin
from .models import User, Dish, MealHistory, Device

admin.site.register(User)
admin.site.register(Dish)
admin.site.register(MealHistory)
admin.site.register(Device)