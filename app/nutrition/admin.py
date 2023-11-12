from django.contrib import admin

# Register your models here.
from .models import FoodCategory, FoodItem, Journal, JournalItem, TargetIntake

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

class JournalItemInline(admin.TabularInline):
    model = JournalItem
    extra = 1

class JournalAdmin(admin.ModelAdmin):
    inlines = [JournalItemInline,]
    list_filter = ["date",]
    ordering = ["-date",]

class TargetIntakeAdmin(admin.ModelAdmin):
    list_display = [
        "name", "energy", "fat", "protein", "active",
    ]

admin.site.register(FoodCategory, FoodCategoryAdmin)
admin.site.register(FoodItem, FoodItemAdmin)
admin.site.register(Journal, JournalAdmin)
admin.site.register(JournalItem)
admin.site.register(TargetIntake, TargetIntakeAdmin)
