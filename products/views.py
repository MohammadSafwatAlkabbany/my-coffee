from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.
def products(request):
    pro=Product.objects.all()
    name= None
    desc= None
    pfrom= None
    pto=None
    cs='off'
    if 'cs' in request.GET:
        cs=request.GET['cs']
        

    if 'SearchName' in request.GET:
       name=request.GET['SearchName']
       if name:
           if cs=='on':
               pro = pro.filter(name__contains=name)
           else:
               pro = pro.filter(name__icontains=name)

    if 'SearchDescrip' in request.GET:
        desc =request.GET['SearchDescrip']
        if desc:
            if cs=='on':
                pro= pro.filter(description__contains=desc)
            else:
                pro= pro.filter(description__icontains=desc)
                
    if 'SearchPriceFrom' in request.GET and 'SearchPriceTo' in request.GET:
        pfrom= request.GET['SearchPriceFrom']
        pto= request.GET['SearchPriceTo']  
        if pfrom and pto:
            if pfrom.isdigit() and pto.isdigit():
                pro= pro.filter(price__gte=pfrom, price__lte=pto)  
    
    context={
     'products' : pro
     
    }
    return render(request, 'products/products.html', context)

def product(request, pro_id):
    context={
        'pro':get_object_or_404(Product, pk=pro_id)
    }
    return render(request, 'products/product.html', context)

def search(request):
    return render(request, 'products/search.html')