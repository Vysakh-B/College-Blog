from django.shortcuts import render,redirect,get_object_or_404
# from .forms import UserRegistrationForm
from django.contrib import messages
# from .forms import LoginForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User,auth
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
from . models import Profile
from posts.models import post,Bookmark
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model




# Create your views here.

def logout(request):
    # Call Django's built-in logout function to clear the session and log out the user
    auth_logout(request)
    
    return redirect('index')  # Change 'login' to the name of your login page URL
def index(request):
    # ch = request.user
    # prf = Profile.objects.get(username=ch)
    # change = prf.accepted
    pst = post.objects.filter(status='Approved',showing=True)[:4]
    return render(request,'index.html',{'key':pst})
    # return render(request,'index.html')    

def signin(request):
    if request.method=='POST':
        username=request.POST['username']
        pswd=request.POST['password']
        flg = False
        user=auth.authenticate(username=username,password=pswd)
        print(user)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            flg=True
            data = 'invalid credentials'
            # return redirect('signin')
            return render (request,'signin.html',{ 'data': data,'fg':flg })

    return render (request,'signin.html')


 
def about(request):
    return render(request,'about.html')
def ctct(request):
    return render(request,'contact.html')

def home(request):
    ch = request.user
    bookset=[]
    prf = Profile.objects.get(username=ch)
    Book = Bookmark.objects.filter(userid=prf.id)
    for i in Book:
        bookset.append(i.postid.id)
    change = prf.accepted
    # pst = post.objects.all()
    pst = post.objects.filter(status='Approved',showing=True)
    # print(bookset)
    return render(request,'home.html',{'pased':change,'key':pst,'ck':bookset})
    
def register(request):
    if request.method == 'POST':
        username = request.POST['username'] 
        email = request.POST['email']
        password = request.POST['password']
        department = request.POST['department']
        reg =  request.POST['register_no']
        ch = False 
        if User.objects.filter(username=username).exists():
            print('email already exist!!')
            err = "user already exists"
            ch = True
            # return redirect('register')
            return render(request,'register.html',{'data':err,'chk':ch })

            

                    
        else:

            user=User.objects.create_user(username = username,email=email,password=password)
            print(username)
            user.save()
            if reg == "":
                reg="NONE"
            prf = Profile.objects.create(username=username,email=email,department=department,register_no=reg)
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
        'name':prf.username,
        'dpt' :prf.department
    }
    
    pst = post.objects.filter(user=prf,status='Approved',showing=True)
    pending_post = post.objects.filter(user=prf,status='Pending')
    rejected_post = post.objects.filter(user=prf,status='Rejected',showing=True)

    # context2={
    #     'ttl':pst.title,
    #     'cnt':pst.content,
    #     'pics':pst.blog_picture,
    #     'dates':pst.created_at
    # }
    return render(request,'profile.html',{'context':context,'key':pst,'wait':pending_post,'reject':rejected_post})