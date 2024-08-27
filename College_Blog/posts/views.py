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
        dis = ""
        tg=False
        us = request.user
        fil = Profile.objects.get(username=us)
        title = request.POST['title']
        content = request.POST['content']
        image = request.FILES.get('imgs')
        if image:
            # Validate file size (e.g., max 5MB)
            max_size = 5 * 1024 * 1024  # 5MB
            if image.size > max_size:
                tg=True
                dis = "Image file too large ,Consider less than 5 MB"
                return render(request,'create.html',{'err': dis,'ck':tg }) # Redirect back to the create page

            # Validate file type (e.g., only allowing JPEG and PNG)
            valid_mime_types = ['image/jpeg']
            if image.content_type not in valid_mime_types:
                tg=True
                dis = "Unsupported file type. Only JPEG and PNG are allowed"
                return render(request,'create.html',{'err': dis,'ck':tg }) # Redirect back to the create page
        post.objects.create(user=fil,title=title,content=content,blog_picture=image)
        return redirect('home')
    return render(request,'create.html') 
def search(request):
    return render(request,'search.html')
def edit(request):
    if request.method == 'POST':
        # user = User.objects.get(id=request.session.get('ids'))
        dis = ""
        tg=False
        us = request.user
        bio = request.POST['bio']
        image = request.FILES.get('pimgs')
        if image:
            # Validate file size (e.g., max 5MB)
            max_size = 5 * 1024 * 1024  # 5MB
            if image.size > max_size:
                tg=True
                dis = "Image file too large ,Consider less than 5 MB"
                return render(request,'edit.html',{'err': dis,'ck':tg }) # Redirect back to the create page

            # Validate file type (e.g., only allowing JPEG and PNG)
            valid_mime_types = ['image/jpeg','image/png']
            if image.content_type not in valid_mime_types:
                tg=True
                dis = "Unsupported file type. Only JPEG and PNG are allowed"
                return render(request,'edit.html',{'err': dis,'ck':tg }) # Redirect back to the create page
        # Get the current user's profile
        profile = Profile.objects.get(username=us)

        # Update the bio field
        profile.bio = bio

        # Update the profile_picture field if a new picture is uploaded
        if image:
            profile.profile_picture = image

        # Save the updated profile
        profile.save()
        return redirect('home')
    # return render(request,'create.html') 
    return render(request,'edit.html')