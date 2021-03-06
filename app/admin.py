from app.models import *
from django.contrib.auth.models import User
from django.contrib import admin

class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "thumbnail", "id", "price", "point", "category", "supplier", "amount"]
    search_fields = ["name"]
    readonly_fields = ["id"]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]
    search_fields = ["name"]
    readonly_fields = ["id"]

class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "status","total_price","total_point", "timestamp",
                    "addr_firstline", "addr_secondline", "addr_town","addr_country",
                    "addr_zipcode"]
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

class UserProfileAdmin(admin.ModelAdmin) :
    list_display = ["user"]
    readonly_fields = ["id"]

class SupplierAdmin(admin.ModelAdmin):
    list_display = ["company_name", "id", "contact"]
    search_fields = ["company_name"]
    readonly_fields = ["id"]    
    
#Arm Add

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ProductInOrder, ProductInOrderAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)