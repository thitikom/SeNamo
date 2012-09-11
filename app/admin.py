from app.models import Product, Category, UserProfile
from django.contrib.auth.models import User
from django.contrib import admin

class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "thumbnail", "id", "price", "point", "category"]
    search_fields = ["name"]
    readonly_fields = ["id"]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]
    search_fields = ["name"]
    readonly_fields = ["id"]

class UserProfInline(admin.StackedInline):
    model = UserProfile

class UserAdmin(admin.ModelAdmin):
    inlines = [UserProfInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)