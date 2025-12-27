from django.contrib import admin
from django.utils.html import format_html
from .models import Category, MenuItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_order']
    list_editable = ['display_order']

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'image_preview']
    list_filter = ['category', 'is_available']
    list_editable = ['price', 'is_available']
    readonly_fields = ['image_preview']

    @admin.display(description='Image')
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:80px;border-radius:8px;" />',
                obj.image.url
            )
        return "—"