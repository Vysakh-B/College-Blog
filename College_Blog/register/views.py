from django.shortcuts import render,redirect,get_object_or_404
# from .forms import UserRegistrationForm
from django.contrib import messages
# from .forms import LoginForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User,auth

# from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
from . models import Profile
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model




# Create your views here.
def superu(request):
    return render(request,'super.html')
def logout(request):
    # Call Django's built-in logout function to clear the session and log out the user
    auth_logout(request)
    
    return redirect('index')  # Change 'login' to the name of your login page URL
def index(request):
    return render(request,'index.html')    

def signin(request):
    if request.method=='POST':
        username=request.POST['username']
        pswd=request.POST['password']
        
        user=auth.authenticate(username=username,password=pswd)
        print(user)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.info(request,'invalid credentials')
            return redirect('signin')
    return render (request,'signin.html')


 
def about(request):
    return render(request,'about.html')
def ctct(request):
    return render(request,'contact.html')

def home(request):
    ch = request.user
    prf = Profile.objects.get(username=ch)
    change = prf.accepted
    return render(request,'home.html',{'pased':change})
      

# def account(request):
#     # User = get_user_model()
#     userid = request.session.get('ids')
#     user = User.objects.get(id=userid)
#     return render(request, 'profile.html', {'bio': user.bio,'pic':user.profile_picture})
def register(request):
    if request.method == 'POST':
        username = request.POST['username'] 
        email = request.POST['email']
        password = request.POST['password']
        department = request.POST['department']  
        if User.objects.filter(username=username).exists():
            print('email already exist!!')
            messages.info(request,"user already exists")
            return redirect('register')
            

                    
        else:

            user=User.objects.create_user(username = username,email=email,password=password)
            print(username)
            user.save()
            prf = Profile.objects.create(username=username,email=email,department=department)
            prf.save()
            return redirect('signin')
            # return render(request,'register.html')

    return render(request,'register.html')
def account(request):
    user = request.user
    prf = Profile.objects.get(username=user)
    # print(prf.bio)
    context={
        'bio':prf.bio,
        'pic':prf.profile_picture.url,
        'name':prf.username
    }
    return render(request,'profile.html',context)