from app.models import Product, Category
from django.contrib import admin

class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "thumbnail", "id", "price", "point", "category"]
    search_fields = ["name"]
    readonly_fields = ["id"]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]
    search_fields = ["name"]
    readonly_fields = ["id"]

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)