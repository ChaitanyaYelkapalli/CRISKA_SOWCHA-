from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'category', 'price', 'is_archived', 'archived_date')
    list_filter = ('category', 'is_archived')
    search_fields = ('name',)
    ordering = ('-created_at',)

    actions = ['restore_products']

    def restore_products(self, request, queryset):
        queryset.update(is_archived=False, archived_date=None)

    restore_products.short_description = "Restore selected products"