from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth.models import User
from .models import Profile
from .forms import *
from dashboard.models import *

# LOGIN user to application
def loginUser(request):

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        
        try:
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            message.error(request, 'Username does not exist')
        
        try:
          user = authenticate(request, username=User.objects.get(email=username), password=password)
        except:
          user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')
    
    # return render(request, 'user/login.html')
    return render(request, 'user/authentication/flows/basic/sign-in.html')

def logoutUser(request):
    logout(request) #delete session
    messages.success(request, 'Logout success')
    return redirect('home')

# Register user to application
def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "User account was created!")
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occurred during registration")

    context = {
        'page': page,
        'form': form,
    }
    # return render(request, 'user/register.html', context)
    return render(request, 'user/authentication/flows/basic/sign-up.html', context)

@login_required(login_url="login")
def home(request):
    profile = request.user.profile
    name = request.user.first_name
    email = request.user.email
    record_list = profile.rekodharga_set.all()
    total_record_list = len(record_list)
    print(total_record_list)
    recordblockchain_list = RekodBlokchain.objects.all()
    total_block = len(recordblockchain_list)
    print(total_block)
    context = {
        'total_record_list' : total_record_list,
        'total_block' : total_block,
        'recordblockchain_list' : recordblockchain_list,
        'name': name,
        'email': email,
    }
    return render(request, 'index.html', context)

# @login_required(login_url="login")
# def account(request):
#     profile = request.user.profile
#     name = request.user.first_name
#     form = ProfileForm(instance=profile)

#     if request.method == "POST":
#         form = ProfileForm(request.POST, instance=profile)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Update Profile Success")
#             return redirect('account')

#     context = {
#         'name': name,
#         'form': form,
#     }
#     return render(request, 'user/account.html', context)


