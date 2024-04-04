from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.models import Product
from tags.models import TaggedItem
from store.admin import ProductAdmin

# Register your models here.

class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem

class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)