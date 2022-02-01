from django.contrib.auth import models
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth 
from .models import UserProfile
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from products.models import Product
import re

# Create your views here.

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('index')

def signin(request):
    if request.method =='POST' and 'btnlogin' in request.POST:
         username= request.POST['Username']
         password= request.POST['Password']
         user=auth.authenticate(username=username,password=password)
         if user is not None:
             if 'rememberme' not in request.POST:
                 request.session.set_expiry(0)
             auth.login(request,user)
             #messages.success(request,'you are logged in')
         else:
             messages.error(request,'invalid username or password')
         return redirect('signin')
                
    else:
             return render( request , 'accounts/signin.html')

def signup(request):
    if request.method =='POST' and 'btnsign' in request.POST:

        #variables for field
         Fname= None
         Lname= None
         Address1=None
         Address2=None
         City=None
         State=None
         Zip=None
         Email=None
         Username=None
         Password=None
         Terms=None
         Account_added=None

         #Get values from the form
         if 'Fname' in request.POST: Fname = request.POST['Fname']
         else: messages.error(request,'Error in first name')

         if 'Lname' in request.POST: Lname = request.POST['Lname']
         else: messages.error(request,'Error in last name')

         if 'Address1' in request.POST: Address1 = request.POST['Address1']
         else: messages.error(request,'Error in address1')

         if 'Address2' in request.POST: Address2 = request.POST['Address2']
         else: messages.error(request,'Error in address2')

         if 'City' in request.POST: City = request.POST['City']
         else: messages.error(request,'Error in city')

         if 'State' in request.POST: State = request.POST['State']
         else: messages.error(request,'Error in State')

         if 'Zip' in request.POST: Zip = request.POST['Zip']
         else: messages.error(request,'Error in zip code')

         if 'Email' in request.POST: Email = request.POST['Email']
         else: messages.error(request,'Error in email')

         if 'Username' in request.POST: Username = request.POST['Username']
         else: messages.error(request,'Error in User name')

         if 'Password' in request.POST: Password = request.POST['Password']
         else: messages.error(request,'Error in password')

         if 'Terms' in request.POST: Terms = request.POST['Terms']

         if Fname and Lname and Address1 and Address2 and City and State and Zip and Email and Username and Password:
             if Terms=='on':
                # check for user name   
                if User.objects.filter(username=Username).exists():
                    messages.error(request, ' User name is already exist')
                else:
                    # check the email
                    if User.objects.filter(email=Email).exists():
                         messages.error(request, ' email is already exist')
                    else:
                        #pattern1="^\w+([-+.']\w)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$" 
                        #if re.match(pattern1,Email):
                            
                        #else:
                        #    messages.error(request,'Invalid Email')

                        try:
                           validate_email(Email)
                           user=User.objects.create_user(first_name= Fname, 
                           last_name=Lname, email=Email, username= Username, 
                           password=Password)
                           user.save()

                           userprofile=UserProfile(user=user, address1= Address1,
                           address2=Address2, city=City, state=State, zip_number=Zip)
                           userprofile.save()
                           messages.success(request,'Your account is created')
                           Account_added=True
                           #return redirect('signup')
                           
                        except ValidationError:
                             messages.error(request,'Invalid Email')

             else:
                 messages.error(request, ' You must agree to the terms')

         else:
                messages.error(request, 'check empty fields')

         
         #return redirect('signup') 
         return render( request , 'accounts/signup.html',{
             'Fname':Fname,
             'Lname':Lname,
             'Address1':Address1,
             'Address2':Address2,
             'City':City,
             'State':State,
             'Zip':Zip,
             'Email':Email,
             'Username':Username,
             'Password':Password,
             'Account_added':Account_added

         })       
    else: 
        #Account_added=None       
        return render( request , 'accounts/signup.html')

def profile(request):
    if request.method == 'POST' and 'btnsave' in request.POST:
        

        if request.user is not None and request.user.id !=None:
            userprofile = UserProfile.objects.get(user=request.user)

            if request.POST['Fname'] and request.POST['Lname'] and request.POST['Address1'] and request.POST['Address2'] and request.POST['City'] and request.POST['State'] and request.POST['Zip'] and request.POST['Email'] and request.POST['Username'] and request.POST['Password'] :
                request.user.firstname = request.POST['Fname']
                request.user.lastname = request.POST['Lname']
                userprofile.address1 = request.POST['Address1']
                userprofile.address2 = request.POST['Address2']
                userprofile.city = request.POST['City']
                userprofile.state = request.POST['State']
                userprofile.zip_number = request.POST['Zip']
                #request.user.email = request.POST['Email']
                #request.user.username = request.POST['Username']
                if not request.POST['Password'].startswith('pbkdf2_sha256$'):
                   request.user.set_password(request.POST['Password'])
                request.user.save()
                userprofile.save()
                auth.login(request,request.user)
                messages.success(request,'your data have been saved')
            else:
                messages.error(request, 'check your values')
        return redirect('profile')
    else:
     #   if request.user.is_anonymous:     return redirect('index')
        if request.user is not None:
            context = None
            if request.user.id !=None:
    
                 
                 userprofile=UserProfile.objects.get(user=request.user)
                 context ={
                    'Fname':request.user.first_name,
                    'Lname':request.user.last_name,
                    'Address1':userprofile.address1,
                    'Address2':userprofile.address2,
                    'City':userprofile.city,
                    'State':userprofile.state,
                    'Zip':userprofile.zip_number,
                    'Email':request.user.email,
                    'Username':request.user.username,
                    'Password':request.user.password


                   }
            

            return render( request , 'accounts/profile.html', context)
        else:
                 return redirect('profile')


def product_favourite(request, pro_id):
    if request.user.is_authenticated and request.user.id !=None:
        pro_fav= Product.objects.get(pk=pro_id)
        if UserProfile.objects.filter(user=request.user, product_favourite=pro_fav).exists():
            messages.success(request, 'Product already exists in your favourite list')
        else:
            userprofile=UserProfile.objects.get(user=request.user)
            userprofile.product_favourite.add(pro_fav)
            messages.success(request, 'Product is added to your favourite list') 
    else:
         messages.error(request, 'You must be logged in')    
    
    return redirect('/products/' + str(pro_id))

def show_product_favourite(request):
    context= None
    if request.user.is_authenticated and request.user.id !=None:
        UserInfo=UserProfile.objects.get(user=request.user)
        pro=UserInfo.product_favourite.all()
        context = {'products': pro}
    return render(request, 'products/products.html',context)

