from django.shortcuts import render,redirect
# from .forms import UserRegistrationForm
from django.contrib import messages
from register.models import Profile
# from .forms import LoginForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User,auth


# Create your views here.
def superu(request):
    if request.method=='POST':
        username=request.POST['username']
        pswd=request.POST['password']
        flg = False
        user=auth.authenticate(username=username,password=pswd)
        print(user)
        if user is not None:
            auth.login(request,user)
            try:
                ishere = Profile.objects.get(username=username, is_admin=True)
                # If the user exists and is an admin, redirect to home
                return redirect('adminhome')
            except Profile.DoesNotExist:
                flg=True
                data = 'invalid credentials'
                # return redirect('signin')
                return render (request,'super.html',{ 'data': data,'fg':flg })
        else:
            flg=True
            data = 'invalid credentials'
            # return redirect('signin')
            return render (request,'super.html',{ 'data': data,'fg':flg })

    return render(request,'super.html')
def adminhome(request):
    return render(request,'admin_home.html')