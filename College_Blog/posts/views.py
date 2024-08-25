from django.shortcuts import render,redirect
from . models import post
from django.contrib.auth.models import User
from register.models import Profile

from django.contrib.auth import get_user_model

# Create your views here.
def magazine(request):
    return render(request,'magazine.html') 
def single(request,id):
    if request.user.is_authenticated:     
        u = request.user
        data = Profile.objects.get(username=u)
        pt = post.objects.get(id=id)
        return render(request,'blog-single.html',{'detail':pt,'data':data})
    else:
        return redirect('/signin')
    
def feed(request):
    return render(request,'feed.html') 
def create(request):
    if request.method == 'POST':
        # user = User.objects.get(id=request.session.get('ids'))
        us = request.user
        fil = Profile.objects.get(username=us)
        title = request.POST['title']
        content = request.POST['content']
        blog_picture = request.FILES.get('imgs')
        post.objects.create(user=fil,title=title,content=content,blog_picture=blog_picture)
        return redirect('home')
    return render(request,'create.html') 
def search(request):
    return render(request,'search.html')
def edit(request):
    return render(request,'edit.html')