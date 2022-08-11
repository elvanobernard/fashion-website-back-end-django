from django.contrib import admin
from .models import Category, Product, ProductImage, User, Review, Stock
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'show_in_main')
    prepopulated_fields =  {'slug' : ('category',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(User)
admin.site.register(Review)
admin.site.register(Stock)