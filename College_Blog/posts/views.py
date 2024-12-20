from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from . models import post,Comment,Bookmark,Likes
from django.contrib.auth.models import User
from register.models import Profile
from django.apps import apps
from django.contrib.auth import get_user_model

# Create your views here.

def single(request,id):
    if request.user.is_authenticated:     
        u = request.user
        likeset = []
        pt = post.objects.get(id=id)
        Magazine = apps.get_model('super', 'Magazine')
        magazine_post_ids = set(Magazine.objects.values_list('post_id', flat=True))
        data = Profile.objects.get(username=pt.user)
        chk = Profile.objects.get(username=u)
        related = post.objects.filter(user=pt.user,status="Approved").exclude(id=pt.id)[:3]
        # cmnts = Comment.objects.filter(post_id=id).select_related('user_id__profile').order_by('commented_at')[:3]
        cmnts = Comment.objects.filter(post_id=id).select_related('user_id').order_by('-commented_at')[:2]
        cmnt_count = cmnts.count()
        lks = Likes.objects.filter(post_id=id)
        likes_count = lks.count()
        Book = Likes.objects.filter(user_id=chk,post_id=id)
        # for i in Book:
        #     likeset.append(i.post_id)
        # context = {
        # 'comments': cmnts,
        # 'post': pt,  # Example: the post itself
        #             }
        return render(request,'blog-single.html',{'detail':pt,'data':data,'check':chk,'related':related,'cmntss':cmnts,'cnt1':cmnt_count,'cnt2':likes_count,'ck':Book,'magz':magazine_post_ids})
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
    pst = post.objects.filter(status='Approved',showing=True)
    return render(request,'feed.html',{'pased':change,'key':pst})
    
def create(request):
    if request.method == 'POST':
        # user = User.objects.get(id=request.session.get('ids'))
        dis = ""
        tg=False
        us = request.user
        fil = Profile.objects.get(username=us)
        title = request.POST['title'].strip()
        content = request.POST['content'].strip()
        image = request.FILES.get('imgs')
        if not title:
            tg = True
            dis = "Title is required."
            return render(request, 'create.html', {'err': dis, 'ck': tg})

            # Check if content is provided
        if not content:
            tg = True
            dis = "Content is required."
            return render(request, 'create.html', {'err': dis, 'ck': tg})

        # Check if image is provided
        if not image:
            tg = True
            dis = "Image is required."
            return render(request, 'create.html', {'err': dis, 'ck': tg})

        if image:
            # Validate file size (e.g., max 5MB)
            max_size = 5 * 1024 * 1024  # 5MB
            if image.size > max_size:
                tg=True
                dis = "Image file too large ,Consider less than 5 MB"
                return render(request,'create.html',{'err': dis,'ck':tg }) # Redirect back to the create page

            # Validate file type (e.g., only allowing JPEG and PNG)
            valid_mime_types = ['image/jpeg','image/png']
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
    query = request.GET.get('srch')
    if query:
        posts=post.objects.filter(title__icontains=query,showing=True,status="Approved")
    return render(request,'search.html',{'items':posts,'qry':query})
def edit(request):
    dis = ""
    tg = False
    us = request.user
    bio = request.POST.get('bio','')
    image = request.FILES.get('pimgs')

    # Check if the bio is empty
    if not bio.strip():  # Ensures bio isn't just whitespace
        tg = True
        dis = "Bio cannot be empty."
        return render(request, 'edit.html', {'err': dis, 'ck': tg})  # Redirect back with error

    # If an image is provided, validate its size and type
    if image:
        # Validate file size (e.g., max 5MB)
        max_size = 5 * 1024 * 1024  # 5MB
        if image.size > max_size:
            tg = True
            dis = "Image file too large. Please use an image less than 5 MB."
            return render(request, 'edit.html', {'err': dis, 'ck': tg})  # Redirect back with error

        # Validate file type (e.g., only allowing JPEG and PNG)
        valid_mime_types = ['image/jpeg', 'image/png']
        if image.content_type not in valid_mime_types:
            tg = True
            dis = "Unsupported file type. Only JPEG and PNG are allowed."
            return render(request, 'edit.html', {'err': dis, 'ck': tg})  # Redirect back with error

    # Get the current user's profile
    profile = Profile.objects.get(username=us)

    # Update the bio field
    profile.bio = bio

    # Update the profile_picture field if a new picture is uploaded
    if image:
        profile.profile_picture = image

    # Save the updated profile
    profile.save()
    dis = "Profile updated succesfully."
    return render(request, 'edit.html', {'err': dis, 'ck': tg})  # Redirect back with error
    
    # return redirect('home')

    # If GET request, render edit form
    return render(request, 'edit.html')

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
        comment = request.POST.get('comment').strip()
    
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
def booked(request):
    us = request.user
    
    user_profile = Profile.objects.get(username=request.user)

    # Fetch all bookmarked posts for the current user
    bookmarked_posts = post.objects.filter(bookmarked_by__userid=user_profile)
    bookset=[]
    prf = Profile.objects.get(username=us)
    Book = Bookmark.objects.filter(userid=prf.id)
    for i in Book:
        bookset.append(i.postid.id)
    return render(request,'bookmarked.html',{'books':bookmarked_posts,'ck':bookset})
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
def bookmark(request,id):
    if request.method == 'POST':

        if request.user.is_authenticated:
            profile = Profile.objects.get(username=request.user)
            post_obj = get_object_or_404(post, id=id)

            # Check if the bookmark already exists
            bookmark, created = Bookmark.objects.get_or_create(userid=profile, postid=post_obj)
        
            if created:
                # If a new bookmark was created
                return JsonResponse({'status': 'added', 'message': 'Bookmark added successfully.'})
            else:
                # If the bookmark already exists, delete it to unbookmark
                bookmark.delete()
                return JsonResponse({'status': 'removed', 'message': 'Bookmark removed successfully.'})
    
        # If the user is not authenticated
        return JsonResponse({'status': 'error', 'message': 'User not authenticated.'}, status=401)
def singleprofile(request,id):
    prf = Profile.objects.get(id=id)
    context={
        'bio':prf.bio,
        'pic':prf.profile_picture.url,
        'name':prf.username,
        'dpt' :prf.department
    }
    
    pst = post.objects.filter(user=prf,status='Approved',showing=True)
    print(len(pst))
    return render(request,'single_profile.html',{'context':context,'lists':pst})
def toggle_like(request,id):
    try:
        # post_id = request.POST.get('post_id')  # Get the post ID from the request
        post_instance = post.objects.get(id=id)  # Fetch the post instance
        profile_instance = Profile.objects.get(username=request.user)  # Get the user's profile

        # Try to get an existing like or create a new one
        like, created = Likes.objects.get_or_create(user_id=profile_instance, post_id=post_instance)

        if created:
            liked = True  # New like created
        else:
            like.delete()  # Delete existing like to "unlike" the post
            liked = False

        return JsonResponse({'liked': liked})
    except post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)  # Handle post not found
    except Exception as e:
        logger.error(f"Error in toggle_like view: {e}")  # Log unexpected errors
        return JsonResponse({'error': 'Internal server error'}, status=500)
    