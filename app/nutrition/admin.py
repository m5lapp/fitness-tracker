from django.contrib import admin

# Register your models here.
from .models import FoodCategory, FoodItem, Meal, MealItem, TargetIntake

class FoodCategoryAdmin(admin.ModelAdmin):
    ordering = ["name",]

class FoodItemAdmin(admin.ModelAdmin):
    list_display = [
        "favourite", "name", "category", "subcategory", "brand", "range",
    ]
    list_display_links = ["favourite", "name",]
    list_filter = ["category",]
    search_fields = ["name", "subcategory", "brand", "range",]
    ordering = [
        "-favourite", "category__name", "subcategory", "brand", "range", "name",
    ]

class MealItemInline(admin.TabularInline):
    model = MealItem
    extra = 2

class MealAdmin(admin.ModelAdmin):
    inlines = [MealItemInline,]
    list_display = ["date", "type",]
    list_filter = ["date", "type",]
    ordering = ["-date",]

class TargetIntakeAdmin(admin.ModelAdmin):
    list_display = [
        "name", "energy", "fat", "protein",
    ]

admin.site.register(FoodCategory, FoodCategoryAdmin)
admin.site.register(FoodItem, FoodItemAdmin)
admin.site.register(Meal, MealAdmin)
admin.site.register(MealItem)
admin.site.register(TargetIntake, TargetIntakeAdmin)
