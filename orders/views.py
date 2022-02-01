from datetime import time
from functools import total_ordering
from django.core.checks import messages
from django.shortcuts import render , redirect
from products.models import Product
from orders.models import Orders , OrderDetails
from .models import Payment
from django.utils import timezone
from django.contrib import messages

def add_to_cart(request):
   if 'pro_id' in request.GET and 'qty' in request.GET and 'price' in request.GET and request.user.is_authenticated and request.user.id !=None: 
       pro_id = request.GET['pro_id']
       qty = request.GET['qty']
       price=request.GET['price']
       order = Orders.objects.all().filter(user=request.user, is_finished=False)
       pro=Product.objects.get(id=pro_id)
       if order:
          old_order = Orders.objects.get(user=request.user, is_finished=False)
          if OrderDetails.objects.all().filter(order=old_order,product_id=pro_id).exists():
             orderdetails=OrderDetails.objects.get(order=old_order,product_id=pro_id)
             orderdetails.Quantity+=int(qty)
             orderdetails.save()
          else:
             orderdetails= OrderDetails.objects.create(product=pro, order=old_order, price=pro.price, Quantity=qty)
          messages.success(request,'The item is added to your order')
       else:
          new_order=Orders()
          new_order.user=request.user
          new_order.order_date=timezone.now()
          new_order.is_finished=False
          new_order.save()
          #orderdetails= OrderDetails.objects.create(product=pro, order=new_order, price=pro.price, quantity=qty)
          orderdetails=OrderDetails()
          orderdetails.product=pro
          orderdetails.order=new_order
          orderdetails.price=pro.price
          orderdetails.Quantity=qty
          orderdetails.save()
          messages.success(request,'a new order is created')
       return redirect('/products/'+ request.GET['pro_id'])
   else:
       if 'pro_id' in request.GET:
          messages.error(request, ' You must be login first ')
          return redirect('/products/'+ request.GET['pro_id'])
       else:
          return redirect(' index ')

def cart(request):
   context=None
   if request.user.is_authenticated and request.user.id !=None:
      if Orders.objects.all().filter(user=request.user, is_finished=False):
         order=Orders.objects.all().get(user=request.user, is_finished=False)
         orderdetails=OrderDetails.objects.all().filter(order=order)
         total=0
         for sub in orderdetails:
            total+= sub.price * sub.Quantity
         context= {
            'order': order,
            'orderdetails' : orderdetails,
            'total': total,
         }
   return render(request, 'orders/cart.html',context)

def remove_from_cart(request,orderdetails_id): 
   if request.user.is_authenticated and request.user.id !=None and orderdetails_id:
      #messages.success(request, 'Product is deleted')
      #orderdetails_id=request.GET['orderdetails_id']
      orderdetails=OrderDetails.objects.get(id=orderdetails_id)
      if orderdetails.order.user.id== request.user.id:
         orderdetails.delete()
   
   return redirect('cart')

def add_qty(request,orderdetails_id): 
   if request.user.is_authenticated and request.user.id !=None and orderdetails_id:
      orderdetails=OrderDetails.objects.get(id=orderdetails_id)
      
      if orderdetails.order.user.id== request.user.id:
         orderdetails.Quantity +=1
         orderdetails.save()
   
   return redirect('cart')

def sub_qty(request,orderdetails_id): 
   if request.user.is_authenticated and request.user.id !=None and orderdetails_id:
      orderdetails=OrderDetails.objects.get(id=orderdetails_id)
      if orderdetails.order.user.id== request.user.id:
         if orderdetails.Quantity>1: 
            orderdetails.Quantity -=1
            orderdetails.save()
         else:
            orderdetails.delete()
   
   return redirect('cart')

def payment(request):
   context=None
   shipment_address=None
   shipment_phone  =None
   card_number     =None
   expiry_date     =None
   security_code   =None

  # is_added        =None
   if request.method=='POST' and 'btnpayment' in request.POST: 
      if 'shipment_address' in request.POST and 'shipment_phone' in request.POST  and  'card_number' in request.POST and 'expiry_date' in request.POST and 'security_code' in request.POST:
            shipment_address = request.POST['shipment_address']
            shipment_phone = request.POST['shipment_phone']
            card_number     = request.POST['card_number']
            expiry_date     = request.POST['expiry_date']
            security_code   = request.POST['security_code']
            #is_added        = request.POSTis_added,
            if request.user.is_authenticated and request.user.id !=None:
               if Orders.objects.all().filter(user=request.user, is_finished=False):
                  order=Orders.objects.all().get(user=request.user, is_finished=False)
                  payment=Payment(order=order, shipment_address=shipment_address, shipment_phone=shipment_phone, card_number=card_number, expiry_date=expiry_date, security_code=security_code) 
                  payment.save()
                  order.is_finished= True
                  order.save()
                  messages.success(request,'your payment is completed')
      context={
            'shipment_address' : shipment_address,
            'shipment_phone'   : shipment_phone,
            'card_number'      : card_number,
            'expiry_date'      : expiry_date,
            'security_code'    : security_code, 
           }     
   else:
      if request.user.is_authenticated and request.user.id !=None:
         if Orders.objects.all().filter(user=request.user, is_finished=False):
            order=Orders.objects.all().get(user=request.user, is_finished=False)
            orderdetails=OrderDetails.objects.all().filter(order=order)
            total=0
            for sub in orderdetails:
               total+= sub.price * sub.Quantity
            context= {
               'order': order,
               'orderdetails' : orderdetails,
               'total': total,
            }
   return render(request, 'orders/payment.html',context)


def my_orders(request):
   context=None
   all_orders=None
   if request.user.is_authenticated and request.user.id !=None:
         all_orders=Orders.objects.all().filter(user=request.user)
         if all_orders:
            for x in all_orders:
               order=Orders.objects.get(id=x.id)
               orderdetails=OrderDetails.objects.all().filter(order=order)
               total=0
               for sub in orderdetails:
                   total+= sub.price * sub.Quantity
               x.total=total
               x.item_count=orderdetails.count

   context={'all_orders':all_orders}
   return render(request,'orders/myorders.html',context)