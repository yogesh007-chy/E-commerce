from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import re
from .forms import ProfileForm


# Create your views here.

def register(request):
    if request.method=='POST':
        fname=request.POST['first_name']
        lname=request.POST['last_name']
        username=request.POST['username'] #sujan710
        email=request.POST['email_add']
        password=request.POST['password']
        password1=request.POST['password1']
        
        if password1==password:
            if CustomUserModel.objects.filter(username=username).exists():
                messages.error(request,"username  already exists")
                return redirect('register')
            if CustomUserModel.objects.filter(email=email).exists():
                messages.error(request,"email  already exists")
                return redirect('register')
            
            try:
                validate_password(password)
                
                error=[]
                
                if not re.search(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$",password):
                    error.append('your password must contain at least one upper okey case')
                    
                if not re.search(r"\d",password): #0-9
                    error.append('your password must contain at least one digit')
                if not error: 
                    CustomUserModel.objects.create_user(first_name=fname,last_name=lname,email=email,username=username,password=password)
                    messages.success(request,"your account is successfully register !!!")
                    return redirect("register")
                else:
                    for i in error:
                        messages.error(request,i)
                        
                    return redirect('register')
            
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request,error)
                return redirect('register')
        else:
            messages.error(request,'your password and confirm password doesnot match')
            return redirect('register')
          
    return render(request,'account/register.html')





def log_in(request):
    if request.method=='POST':
        username=request.POST.get('username') #sujan710
        password=request.POST.get('password') #sujan
        remember_me=request.POST.get('remember_me') #on None
        
        
        if not CustomUserModel.objects.filter(username=username).exists():
            messages.error(request,'username is not register yet')
            return redirect('login')
            
        
        user=authenticate(username=username,password=password) #
        
        if user is not None:
            login(request,user)
            
            if remember_me:
                request.session.set_expiry(12000000)
            else:
                request.session.set_expiry(0)
            
            next=request.POST.get('next','') #/menu/
            return redirect(next if next else "index")
        else:
            messages.error(request,'password invalid!!!')
            return redirect('login')

    next=request.GET.get('next','')   #/menu/ 
        
    return render(request,'account/login.html',{'next':next})


'''
logout section

'''
def log_out(request):
    logout(request)
    return redirect('login')


'''
Profile section

'''

@login_required(login_url='login')
def profile(request):
    profile,created=Profile.objects.get_or_create(user=request.user)
    form=ProfileForm(instance=profile)
    if request.method == "POST":
        form=ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    context={
        'form':form
    }
    return render(request,'profile/profile.html',context)


@login_required(login_url='login')
def dashboard(request):
    return render(request,'profile/dashboard.html')

@login_required(login_url='login')
def myorder(request):
    if request.method == 'POST':
        phone=request.POST['phone']
        address=request.POST['address']
        cart=request.session.get('cart')
        
        for i in cart:
            product=cart[i]['name']
            quantity=cart[i]['quantity']
            price=cart[i]['price']
            total=float(price) * quantity
            image=cart[i]['image']
            
            order=Order(product=product,quantity=quantity,price=price,image=image,total=total,phone=phone,address=address,user=request.user)
            order.save()
        request.session['cart']={}
        return redirect('myorder')
    
    myorder=Order.objects.filter(user=request.user)
    return render(request,'profile/my_order.html',{'myorder':myorder})


