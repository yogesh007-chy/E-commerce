from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([Offerproduct,Category,SubCategory])

class ProductAdminImage(admin.TabularInline):
    model=ProductImage
    extra=2


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','price','desc','category']
    inlines=[ProductAdminImage]