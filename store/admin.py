from typing import Any
from django.db.models.aggregates import Count
from django.contrib import admin,messages
from django.urls import reverse
from django.utils.html import format_html,urlencode
from django.db.models.query import QuerySet
from django.http import HttpRequest
from . import models

# Register your models here.

class InventoryFilter(admin.SimpleListFilter):
    title = 'Inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10','Low')
        ]
    
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)

# class TagInline(GenericTabularInline):
#     autocomplete_fields = ['tag']
#     model = TaggedItem

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # fields = ['title','slug']
    # exclude = ['promotions']
    # readonly_fields = ['title']
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    actions = ['clear_inventory']
    list_display = ['title','unit_price','inventory_status','collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_filter = ['collection','last_update',InventoryFilter]
    list_select_related = ['collection']
    search_fields = ['title__istartswith']
    # inlines = [TagInline]

    def collection_title(self,product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

    @admin.action(description='Clear inventory')
    def clear_inventory(self,request,queryset:QuerySet[Any]):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.',
            messages.ERROR
        )

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','full_name','first_name','last_name','membership','orders_count']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name','last_name']
    search_fields = ['first_name__istartswith','last_name__istartswith']
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

# class OrderItemInline(admin.TabularInline):
class OrderItemInline(admin.StackedInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    extra = 0

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):  
    list_display = ['id','placed_at','customer']
    inlines = [OrderItemInline]
    autocomplete_fields = ['customer']
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
    search_fields = ['title']

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