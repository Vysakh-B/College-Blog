from django.shortcuts import render,redirect
# from .forms import UserRegistrationForm
from django.contrib import messages
from register.models import Profile
from posts.models import post
from . models import Magazine
# from .forms import LoginForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User,auth
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
    ch = request.user
    prf = Profile.objects.all()
    # change = prf.accepted
    # pst = post.objects.all()
    pst = post.objects.filter(status='Approved')
    return render(request,'admin_home.html',{'key':pst})
def pending(request):
    ch = request.user
    prf = Profile.objects.all()
    # change = prf.accepted
    # pst = post.objects.all()
    pst = post.objects.filter(status='Pending')
    return render(request,'pending_post.html',{'key':pst})
def accept(request,id):
    pos = post.objects.get(id=id)
    pos.status = 'Approved'
    pos.save()
    prf = Profile.objects.all()
    # change = prf.accepted
    # pst = post.objects.all()
    pst = post.objects.filter(status='Pending')
    return render(request,'admin_home.html',{'key':pst})
def magazine(request,id):
    pos = post.objects.get(id=id)
    prf = Profile.objects.all()
    # change = prf.accepted
    pst = post.objects.all()
    Magazine.objects.create(user_id=pos.user,post_id=pos)
    return render(request,'admin_home.html',{'key':pst})
def viewmagazine(request):
    plist=[]
    ulist=[]
    mgs = Magazine.objects.all()
    for j in mgs:
        plist.append(j.post_id)
        ulist.append(j.user_id)
    # change = prf.accepted
    # pst = post.objects.all()
    # pst = post.objects.filter(status='Approved')
    return render(request,'magazine.html',{'key':plist,'u':ulist})
def singlemagazine(request,id):     
    # u = request.user
    pt = post.objects.get(id=id)
    data = Profile.objects.get(username=pt.user)
    # chk = Profile.objects.get(username=u)
    return render(request,'magazine_single.html',{'detail':pt,'data':data})
    
def reject(request,post_id):
    # if request.method == 'POST': 
    #     cmnt =  request.POST['reason'] 
    #     pos = post.objects.get(id=id)
    #     pos.admin_comment = cmnt
    #     pos.save()
    #     prf = Profile.objects.all()
    #     # change = prf.accepted
    #     # pst = post.objects.all()
    #     pst = post.objects.filter(status='Pending')
    #     return render(request,'admin_home.html',{'key':pst})
    # data = request.GET.get('data', '')  # Get the 'data' parameter from the URL
    if request.method == 'POST':
        pst = post.objects.get(id=post_id)
        rejection_reason = request.POST.get('reject_reason')
        
        if rejection_reason:
            # Save the rejection reason in the post model (assuming you have a field for it)
            pst.admin_comment = rejection_reason
            pst.status = 'Rejected'  # Optional: Update the post's status to 'Rejected'
            pst.save()

            # Optionally, show a success message
            # messages.success(request, 'The post has been rejected successfully.')

            psts = post.objects.filter(status='Approved')
            return render(request,'admin_home.html',{'key':psts}) # Redirect back to the blog view page

    psts = post.objects.filter(status='Approved')
    return render(request,'admin_home.html',{'key':psts})
def userpending(request):
    profiles = Profile.objects.filter(accepted=False)
    return render(request,'user_pending.html',{'set':profiles})
def acceptuser(request,id):
    appr = Profile.objects.get(id=id)
    appr.accepted=True
    appr.save()
    profiles = Profile.objects.filter(accepted=False)
    return render(request,'user_pending.html',{'set':profiles})