from django.contrib import admin
from .models import Category, MenuItem, Combo

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_order']
    list_editable = ['display_order']

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available']
    list_filter = ['category', 'is_available']
    list_editable = ['price', 'is_available']

@admin.register(Combo)
class ComboAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_available']
    list_editable = ['price', 'is_available']