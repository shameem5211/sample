from django.shortcuts import render,redirect
from . models import *
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def signup(request):
    if request.method=='POST':
        first_name=request.POST['name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        c_password=request.POST['confirm_password']
        if password==c_password:
            if User.objects.filter(username=username):
                messages.info(request,"username already exists")
                return redirect('signup_page')
            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email already taken")
                return redirect('signup_page')
            else:
                user=User.objects.create_user(
                    first_name=first_name,
                    username=username,
                    email=email,
                    password=password,    
                )
                user.save()
                
                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                
                # create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model)
                new_profile.save()
                print('success')
                return redirect('signin')
        else:
            return redirect('signup')
    else:
        return render(request,'signup.html')
    
    
    
    
def signin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')
    
    return render(request,'signin.html')

@login_required(login_url='signin')
def home(request):
    return render(request,'home.html')

@login_required(login_url='signin')
def user_logout(request):
      auth.logout(request)
      return redirect('signin')