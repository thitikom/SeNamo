from app.models import Product, Category, Order, ProductInOrder, UserProfile
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

class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "status", "timestamp"]
    search_fields = ["user"]
    readonly_fields = ["id"]

class ProductInOrderAdmin(admin.ModelAdmin):
    list_display = ["product", "amount", "order", "status", "ship_time"]
    search_fields = ["product"]
    readonly_fields = ["id"]

class UserProfInline(admin.StackedInline):
    model = UserProfile

class UserAdmin(admin.ModelAdmin):
    inlines = [UserProfInline]


#Arm Add

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ProductInOrder, ProductInOrderAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)