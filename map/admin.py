from django.contrib import admin
from .models import AppUser, Dish, Product, MealHistory, Device

admin.site.register(AppUser)
admin.site.register(Dish)
admin.site.register(Product)
admin.site.register(MealHistory)
admin.site.register(Device)