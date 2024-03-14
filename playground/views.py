from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,F
from django.http import HttpResponse
from store.models import Product

# Create your views here.
# request -> response
# request handler
# action

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
    # queryset = Product.objects.filter(inventory = F('unit_price'))
    # queryset = Product.objects.filter(inventory = F('collection__id'))
    # queryset = Product.objects.order_by('unit_price','-title')
    # product = Product.objects.order_by('unit_price')[0]
    product = Product.objects.earliest('unit_price')    #same result as above earliest return an object while order_by return a query set
    # product = Product.objects.latest('unit_price')
    

    # for product in query_set:
    #     print(product)

    # query_set[0:5]

    # return render(request, 'hello.html', {'name' : '', 'products': list(queryset)})
    return render(request, 'hello.html', {'name' : '', 'product': product})