from typing import Any
from django.db.models.aggregates import Count
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html,urlencode
from django.db.models.query import QuerySet
from django.http import HttpRequest
from . import models

# Register your models here.

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','unit_price','inventory_status','collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']

    def collection_title(self,product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','full_name','first_name','last_name','membership','orders_count']
    list_editable = ['membership']
    ordering = ['first_name','last_name']
    list_per_page = 10
    # list_select_related = ['order_set']

    def full_name(self,customer):
        return f'{customer.first_name} {customer.last_name}'
    
    # @admin.display(ordering='order')
    # def order_id(self,customer):
    #     orders = customer.order_set

    #     # order_id_list = ''
        
    #     # for singleOrder in orders:
    #     #     order_id_list += str(singleOrder)
        
    #     return orders

    @admin.display(ordering='orders_count')
    def orders_count(self,customer):
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({
                'customer_id': str(customer.id)
            })
            )

        return format_html('<a href="{}">{}</a>',url,customer.orders_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count = Count('order')
        )

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):  
    list_display = ['id','placed_at','customer']

    # def customer_details(self,order):
    #     url = (
    #         reverse('admin:store_customer_changelist')
    #         + '?'
    #         + urlencode({
    #             'order_id':str(order.id)
    #         })
    #         )
    #     return format_html('<a href="{}">{}</a>',url,order.customer)
    
    # def get_queryset(self, request):
    #     return super().get_queryset(request).filter(pk='id')

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','products_count']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        # return format_html('<a href="http://google.com">{}</a>',collection.products_count)
        # reverse('admin:app_model_page')
        url = (
                reverse('admin:store_product_changelist') 
               + '?' 
               + urlencode({
                   'collection_id': str(collection.id)
               })
               )
        
        return format_html('<a href="{}">{}</a>',url,collection.products_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count = Count('product')
        )

# admin.site.register(models.Product,ProductAdmin)