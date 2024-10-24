from django.shortcuts import render,redirect
from . models import post,Comment
from django.contrib.auth.models import User
from register.models import Profile

from django.contrib.auth import get_user_model

# Create your views here.

def single(request,id):
    if request.user.is_authenticated:     
        u = request.user
        pt = post.objects.get(id=id)
        data = Profile.objects.get(username=pt.user)
        chk = Profile.objects.get(username=u)
        related = post.objects.filter(user=pt.user,status="Approved").exclude(id=pt.id)[:3]
        # cmnts = Comment.objects.filter(post_id=id).select_related('user_id__profile').order_by('commented_at')[:3]
        cmnts = Comment.objects.filter(post_id=id).select_related('user_id').order_by('-commented_at')[:2]

        # context = {
        # 'comments': cmnts,
        # 'post': pt,  # Example: the post itself
        #             }
        return render(request,'blog-single.html',{'detail':pt,'data':data,'check':chk,'related':related,'cmntss':cmnts})
        if request.method == 'POST': 
            cmnt =  request.POST['comment'] 
            pos = post.objects.get(id=id)
            pos.admin_comment = cmnt
            pos.save()
            prf = Profile.objects.all()
            # change = prf.accepted
            # pst = post.objects.all()
            pst = post.objects.filter(status='Approved')
            return render(request,'admin_home.html',{'key':pst})
    else:
        return redirect('/signin')
    
def feed(request):
    ch = request.user
    prf = Profile.objects.get(username=ch)
    change = prf.accepted
    # pst = post.objects.all()
    pst = post.objects.filter(status='Approved')
    return render(request,'feed.html',{'pased':change,'key':pst})
    
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
def editpost(request,post_id):
    postd = post.objects.get(id=post_id)
    context={
        "title": postd.title,
        "content" :postd.content,
        'img' : postd.blog_picture
    }
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
                return render(request,'edit_post.html',{'err': dis,'ck':tg }) # Redirect back to the create page

            # Validate file type (e.g., only allowing JPEG and PNG)
            valid_mime_types = ['image/jpeg']
            if image.content_type not in valid_mime_types:
                tg=True
                dis = "Unsupported file type. Only JPEG and PNG are allowed"
                return render(request,'edit_post.html',{'err': dis,'ck':tg }) # Redirect back to the create page
        # post.objects.create(user=fil,title=title,content=content,blog_picture=image)
        postd.title=title
        postd.content=content
        postd.blog_picture=image
        postd.status="Pending"
        postd.save()
        return redirect('profile')
    return render(request,'edit_post.html',{'context':context})
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
def addcomment(request,post_id):
    u=request.user
    err = ""
    tg=False
    if request.method == 'POST':
        u=request.user
        err = ""
        tg=False
        prf = post.objects.get(id=post_id)
        prf_id = Profile.objects.get(username=u)
        comment = request.POST.get('comment')
    
        if comment == "":
            tg=True
            err = "Comment must not be blank"
            # Save the rejection reason in the post model (assuming you have a field for it)
            pt = post.objects.get(id=post_id)
            data = Profile.objects.get(username=pt.user)
            chk = Profile.objects.get(username=u)
            return render(request,'blog-single.html',{'detail':pt,'data':data,'check':chk,'er':err,'tg':tg})
            # return render(request,'blog-single.html',{'key':psts}) # Redirect back to the blog view page
        Comment.objects.create(post_id=prf,user_id=prf_id,comment_description=comment)
        tg=False
        err = "Commented Succesfully"
        # Save the rejection reason in the post model (assuming you have a field for it)
        pt = post.objects.get(id=post_id)
        data = Profile.objects.get(username=pt.user)
        chk = Profile.objects.get(username=u)
        related = post.objects.filter(user=pt.user,status="Approved").exclude(id=pt.id)[:3]
        # cmnts = Comment.objects.filter(post_id=id).select_related('user_id__profile').order_by('commented_at')[:3]
        cmnts = Comment.objects.filter(post_id=post_id).select_related('user_id').order_by('-commented_at')[:2]

        # context = {
        # 'comments': cmnts,
        # 'post': pt,  # Example: the post itself
        #             }
        return render(request,'blog-single.html',{'detail':pt,'data':data,'check':chk,'related':related,'cmntss':cmnts})
        # pst.status = 'Rejected'  # Optional: Update the post's status to 'Rejected'
        # cmt.save()
    pt = post.objects.get(id=post_id)
    data = Profile.objects.get(username=pt.user)
    chk = Profile.objects.get(username=u)
    related = post.objects.filter(user=pt.user,status="Approved").exclude(id=pt.id)[:3]
    # cmnts = Comment.objects.filter(post_id=id).select_related('user_id__profile').order_by('commented_at')[:3]
    cmnts = Comment.objects.filter(post_id=post_id).select_related('user_id').order_by('-commented_at')[:2]

    # context = {
    # 'comments': cmnts,
    # 'post': pt,  # Example: the post itself
    #             }
    return render(request,'blog-single.html',{'detail':pt,'data':data,'check':chk,'related':related,'cmntss':cmnts})
def addreport(request,c_id,p_id):
    u=request.user
    # err = ""
    # tg=False
    cmtn = Comment.objects.get(id=c_id)
    cmtn.report_count = cmtn.report_count + 1
    cmtn.save()
    err = "Reported Succesfully"
    # Save the rejection reason in the post model (assuming you have a field for it)
    pt = post.objects.get(id=p_id)
    data = Profile.objects.get(username=pt.user)
    chk = Profile.objects.get(username=u)
    # return render(request,'blog-single.html',{'detail':pt,'data':data,'check':chk,'er':err,'tg':tg})
    
    related = post.objects.filter(user=pt.user,status="Approved").exclude(id=pt.id)[:3]
    # cmnts = Comment.objects.filter(post_id=id).select_related('user_id__profile').order_by('commented_at')[:3]
    cmnts = Comment.objects.filter(post_id=p_id).select_related('user_id').order_by('-commented_at')[:2]

    # context = {
    # 'comments': cmnts,
    # 'post': pt,  # Example: the post itself
    #             }
    return render(request,'blog-single.html',{'detail':pt,'data':data,'check':chk,'related':related,'cmntss':cmnts})
def removepost(request,post_id):
    try:
        rpst = post.objects.get(id=post_id)  # Use get() to get a single object
        rpst.showing = False  # Modify the attribute of the single object
        rpst.save()  # Save the object
    except post.DoesNotExist:
        # Handle the case where the post doesn't exist
        return HttpResponse("Post not found.")
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
def singleview(request,profile_id):
    # user = request.user
    prf = Profile.objects.get(id=profile_id)
    # print(prf.bio)
    context={
        'bio':prf.bio,
        'pic':prf.profile_picture.url,
        'name':prf.username,
        'dpt' :prf.department
    }
    
    pst = post.objects.filter(user=prf,status='Approved',showing=True)
    # pending_post = post.objects.filter(user=prf,status='Pending')
    # rejected_post = post.objects.filter(user=prf,status='Rejected',showing=True)

    # context2={
    #     'ttl':pst.title,
    #     'cnt':pst.content,
    #     'pics':pst.blog_picture,
    #     'dates':pst.created_at
    # }
    return render(request,'profile.html',{'context':context,'key':pst})