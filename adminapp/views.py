from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from . models import *
from myapp.models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound

# Create your views here.


def admin_login(request):
    try:
        if request.user.is_authenticated:
            return redirect('admin_home')
        
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username = username)
            if not user_obj.exists():
                messages.info(request,'Account not found')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            user_obj = authenticate(username=username , password = password)
            
            if user_obj and user_obj.is_superuser:
                login(request,user_obj)
                return redirect('admin_home')
            
            messages.info(request, 'Invalid Password')
            return redirect('admin_home')
        
        return render(request,'admin_login.html')
    
    except Exception as e:
        print(e)

@login_required(login_url='admin_login')
def admin_home(request):
    users = User.objects.filter(is_superuser=False)
    context = {
        'users':users
    }
    return render(request,'admin_home.html',context)


def edit_user(request, user_id):
    try:
        # Ensure that the logged-in user is a superuser
        if not request.user.is_superuser:
            return HttpResponseNotFound("You don't have permission to edit this user.")

        # Fetch the user to edit
        user_to_edit = User.objects.get(id=user_id)

        if request.method == 'POST':
            new_username = request.POST.get('new_username')
            new_first_name = request.POST.get('new_first_name')
            new_email = request.POST.get('new_email')

            # Update user attributes
            user_to_edit.username = new_username
            user_to_edit.first_name = new_first_name
            user_to_edit.email = new_email

            user_to_edit.save()
            messages.success(request, f"User {user_to_edit.username}'s details updated successfully.")
            return redirect('admin_home')

        return render(request, 'edit_user.html', {'user_to_edit': user_to_edit})

    except User.DoesNotExist:
        # Handle the case where the user with the given id does not exist
        return HttpResponseNotFound("User not found")

    except Exception as e:
        # Handle other exceptions
        messages.error(request, f"An error occurred: {e}")
        return redirect('admin_home')
