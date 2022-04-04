from django.contrib import admin
from .models import *


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category']


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['sub_category', 'category']
    list_filter = ['category']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sub_category', 'category']
    list_filter = ['category', 'sub_category']


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'username']


class ApplyAdmin(admin.ModelAdmin):
    list_display = ['customer', 'customer_name', 'customer_phone', 'product', 'date_ordered']
    list_filter = ['customer', 'product']


class About_UsAdmin(admin.ModelAdmin):
    list_display = ['pk', 'about_us']


class ContactAdmin(admin.ModelAdmin):
    list_display = ['pk', 'addresses', 'phone_numbers', 'locations']


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Apply, ApplyAdmin)
admin.site.register(About_Us, About_UsAdmin)
admin.site.register(Contact, ContactAdmin)

