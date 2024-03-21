from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction,connection
from django.db.models import Q,F
from django.db.models import Value,Func,ExpressionWrapper,DecimalField
from django.db.models.functions import Concat
from django.db.models.aggregates import Count,Max,Min,Avg,Sum
from django.http import HttpResponse
from store.models import Product,OrderItem,Order,Customer,Collection
from tags.models import TaggedItem

# Create your views here.
# request -> response
# request handler
# action

# @transaction.atomic()
def say_hello(request):
    # return HttpResponse('Hello World')
    # queryset = Product.objects.all()[:5]

    # query_set = Product.objects.all()
    # try:
    #     product = Product.objects.get(pk=0)
    # except ObjectDoesNotExist:
    #     pass

    # product = Product.objects.filter(pk=0).first()
    # exists = Product.objects.filter(pk=0).exists()

    # queryset = Product.objects.filter(unit_price__gt=20)
    # queryset = Product.objects.filter(unit_price__range=(20,30))
    # queryset = Product.objects.filter(collection__id__range=(1,2,3))
    # queryset = Product.objects.filter(title__icontains='coffee')
    # queryset = Product.objects.filter(last_update__date=2021)
    # queryset = Product.objects.filter(description__isnull=True)
    # queryset = Product.objects.filter(inventory__lt=10,unit_price__lt=20)
    # queryset = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)
    # queryset = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
    # queryset = Product.objects.filter(Q(inventory__lt=10) & ~Q(unit_price__lt=20))
    # queryset = Product.objects.filter(inventory = F('collection__id'))
    # queryset = Product.objects.filter(inventory = F('unit_price'))
    # queryset = Product.objects.order_by('unit_price','-title')
    # product = Product.objects.order_by('unit_price')[0]
    # product = Product.objects.earliest('unit_price')    #same result as above earliest return an object while order_by return a query set
    # product = Product.objects.latest('unit_price')
    # queryset = Product.objects.all()[:5]    # 0,1,2,3,4 
    # queryset = Product.objects.all()[5:10]  # 5,6,7,8,9
    # queryset = Product.objects.values('id','title','collection__title')
    # queryset = Product.objects.values_list('id','title','collection__title')

    # queryset = OrderItem.objects.select_related('product').order_by('product__title').distinct()
    
    # queryset = Order.objects.order_by('-placed_at').values('customer__first_name')[:5]
    # queryset = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]

    # result = Product.objects.aggregate(count=Count('id'),min_price=Min('unit_price'))

    # queryset = Customer.objects.annotate(is_new=Value(True))
    # queryset = Customer.objects.annotate(new_id=F('id')+1)

    # queryset = Customer.objects.annotate(
    #     # CONCAT
    #     full_name = Func(F('first_name') , Value(' ') , F('last_name'),function='CONCAT')
    # )

    # queryset = Customer.objects.annotate(
    #     # CONCAT
    #     full_name = Concat('first_name',Value(' '),'last_name')
    # )

    # queryset = Customer.objects.annotate(
    #     orders_count = Count('order')
    # )

    # discounted_price = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())    
    # queryset = Product.objects.annotate(
    #     discounted_price = discounted_price
    # )

    # content_type = ContentType.objects.get_for_model(Product)

    # queryset = TaggedItem.objects\
    #             .select_related('tag')\
    #             .filter(
    #                 content_type=content_type,
    #                 object_id=1
    #             )
    # queryset = TaggedItem.objects.get_tags_for(Product,1)

    # collection = Collection()
    # collection.title = 'Video Games'
    # collection.featured_product = Product(pk=1)
    # # collection.featured_product_id = 1
    # collection.save()

    # collection = Collection.objects.create(title='a', featured_product_id=1)

    # collection = Collection.objects.get(pk=11)
    # collection.featured_product = None
    # collection.save()

    # Collection.objects.filter(pk=11).update(featured_product=None)

    # Collection.objects.delete(pk=11)

    # with transaction.atomic():
    #     order = Order()
    #     order.customer_id = 1
    #     order.save()

    #     item = OrderItem()
    #     item.order = order
    #     item.product_id = 1
    #     item.quantity = 1
    #     item.unit_price = 10
    #     item.save()

    # queryset = Product.objects.raw('SELECT * FROM store_product')
    with connection.cursor() as cursor:
    # cursor = connection.cursor()
        cursor.execute('SELECT * FROM store_address')  # <-- any sql command
    # cursor.close()

    # queryset = Product.objects.filter(id__in=OrderItem.objects.values('product__id').distinct()).order_by('title')

    # for product in query_set:
    #     print(product)

    # query_set[0:5]

    return render(request, 'hello.html', {'name' : ''})
    # return render(request, 'hello.html', {'name' : '', 'product': product})
    # return render(request, 'hello.html', {'name' : '', 'result': result})