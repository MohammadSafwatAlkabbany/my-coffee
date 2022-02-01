from django.urls import path
from . import views

urlpatterns = [
  path('signin', views.signin, name= 'signin'),
  path('signup', views.signup, name= 'signup'), 
  path('logout', views.logout, name= 'logout'),
  path('profile', views.profile, name= 'profile'),  
  path('product_favourite/<int:pro_id>', views.product_favourite, name='product_favourite'),
  path('show_product_favourite', views.show_product_favourite,name='show_product_favourite'),
]