from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns = [
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('cart', views.cart, name='cart'),
    path('<int:orderdetails_id>', views.remove_from_cart, name='remove_from_cart'),
    path('add_qty<int:orderdetails_id>', views.add_qty, name='add_qty'),
    path('sub_qty<int:orderdetails_id>', views.sub_qty, name='sub_qty'),
    path('payment', views.payment, name='payment'),
    path('my_orders', views.my_orders, name='my_orders'),

]