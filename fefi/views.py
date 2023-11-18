from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
# Create your views here.
from django.shortcuts import redirect, render
from .models import Profile,Fef,Reply
from .forms import FefForm,ProfileEditForm,ReplyForm,UserEditForm
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import Http404
from django.contrib.auth.mixins import PermissionRequiredMixin

def index(request):
    return render(request,'fefi/index.html') 

@login_required
def profiles(request):
    if request.user.is_authenticated:
        profiles=Profile.objects.exclude(user=request.user)
        context={'profiles':profiles}
    return render(request,'fefi/profiles.html',context)
@login_required
def feed(request):
    if request.user.is_authenticated:
        fef=Fef.objects.all().order_by('-date_created')
        fefs=Fef.objects.all().order_by('-date_created')
        form=ReplyForm(request.POST,request.FILES)
        context={'fefs':fefs,'form':form}
    return render(request,'fefi/feed.html',context)    
@login_required
def unfollow(request,pk):
    if request.user.is_authenticated:
        profile=Profile.objects.get(user_id=pk)
        request.user.profile.follows.remove(profile)
        request.user.profile.save()
        return redirect('fefi:follows', profile_id=request.user.id)
@login_required
def follow(request,pk):
    if request.user.is_authenticated:
        profile=Profile.objects.get(user_id=pk)
        request.user.profile.follows.add(profile)
        request.user.profile.save()
        return redirect('fefi:follows',profile_id=request.user.id)
@login_required
def unfollow2(request,pk):
    if request.user.is_authenticated:
        profile=Profile.objects.get(user_id=pk)
        request.user.profile.follows.remove(profile)
        request.user.profile.save()
        return redirect('fefi:followers',profile_id=request.user.id)
       
@login_required
def follow2(request,pk):
    if request.user.is_authenticated:
        profile=Profile.objects.get(user_id=pk)
        request.user.profile.follows.add(profile)
        request.user.profile.save()
        return redirect('fefi:followers',profile_id=request.user.id)   



@login_required
def profile(request,profile_id):
    if request.user.is_authenticated:
        profile=get_object_or_404(Profile,id=profile_id)
        fefs=Fef.objects.filter(profile=profile_id).order_by('-date_created')
        if request.method=='POST':
            current_user_profile=request.user.profile
            data=request.POST
            action=data.get('follow')
            if action=='unfollow':
                current_user_profile.follows.remove(profile)
            elif action=='follow':
                current_user_profile.follows.add(profile) 
            current_user_profile.save() 
            return redirect('fefi:profile',profile_id=profile.id)    
    context={'profile':profile,'fefs':fefs}    
    return render(request,'fefi/profile.html',context)
@login_required
def followers(request,profile_id):
    if request.user.is_authenticated:
        profiles=get_object_or_404(Profile,id=profile_id)

        context={'profiles':profiles}
    return render(request,'fefi/followers.html',context)
@login_required    
def follows(request,profile_id):
    if request.user.is_authenticated:
        profiles=Profile.objects.get(id=profile_id)
        context={'profiles':profiles}
    return render(request,'fefi/follows.html',context)

@login_required
def new_fef(request,profile_id):
    profile=get_object_or_404(User,id=profile_id)
    fefs=Fef.objects.filter(profile=profile).order_by('-date_created')


    if request.method!='POST':
        if profile!=request.user:
            raise Http404
        form=FefForm()
    else:
        form=FefForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            new_fef=form.save(commit=False)
            new_fef.profile=profile
            new_fef.save()
            messages.success(request,('fef added successfully'))
            return redirect('fefi:profile',profile_id=profile_id)
    context={'form':form,'profile':profile,'fefs':fefs}
    return render(request,'fefi/new_fef.html',context)    
@login_required
def photo(request,pk):
    if request.user.is_authenticated:
        profile=Profile.objects.get(user_id=pk)
    if profile is not None:
        return render(request,'fefi/photo.html',{'profile':profile})
    else:
        raise Http404('no photo')
@login_required
def fef_like(request,fef_id):
    if request.user.is_authenticated:
        fef=Fef.objects.get(id=fef_id)
        profile=fef.profile
        if fef.likes.filter(id=request.user.id):
            fef.likes.remove(request.user)
        else:
            fef.likes.add(request.user) 
        return redirect('fefi:profile',profile_id=profile.id)    
@login_required
def fef_like2(request,fef_id):
    if request.user.is_authenticated:
        fef=Fef.objects.get(id=fef_id)
        if fef.likes.filter(id=request.user.id):
            fef.likes.remove(request.user)
        else:
            fef.likes.add(request.user) 
        return redirect('fefi:feed')   
@login_required
def delete_fef(request,fef_id):
    if request.user.is_authenticated:
        fef=get_object_or_404(Fef,id=fef_id)
        profile=fef.profile
        if fef.profile!=request.user:
            raise Http404
        context={'fef':fef,'profile':profile}
        if request.method=='GET':
            return render(request,'fefi/profile.html',context)
        elif request.method=='POST':
            fef.delete()
            messages.success(request,'fef deleted')
            return redirect('fefi:profile',profile_id=profile.id)

@login_required
def search(request):
    if request.method=='POST':
        search=request.POST['search']
        searched=User.objects.filter(username=search)
        return render(request,'fefi/search.html',{'search':search,'searched':searched})
    else:
        return render(request,'fefi/search.html',{}) 
def reply(request,fef_id):
    fef=get_object_or_404(Fef,id=fef_id)
    reply=Reply.objects.filter(fef=fef).order_by('-date_created')
    if request.method!='POST':
        form=ReplyForm()
    else:
        form=ReplyForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            new_reply=form.save(commit=False)
            new_reply.users=request.user
            new_reply.fef=fef
            new_reply.save()
            return redirect('fefi:reply',fef_id=fef.id)
    return render(request,'fefi/reply.html',{'form':form,'fef':fef,'reply':reply}) 
@login_required
def reply_delete(request,reply_id):
    if request.user.is_authenticated:
        #in deleting instances use things referenced in the models like here i used fef=reply.fef, so the reverse can be fef_id=fef.id.it gave me alot of headaches please remember.
        reply=get_object_or_404(Reply,id=reply_id)
        fef=reply.fef
        if reply.users!=request.user:
            raise Http404
        context={'reply':reply}
        if request.method=='GET':
            return render(request,'fefi/reply.html',context)
        elif request.method=='POST':
            reply.delete()
            messages.success(request,'feply deleted')
            return redirect('fefi:reply',fef_id=fef.id)
@login_required
def reply_like(request,reply_id):
    if request.user.is_authenticated:
        fefs=Reply.objects.get(id=reply_id)
        fef=fefs.fef
        if fefs.likes.filter(id=request.user.id):
            fefs.likes.remove(request.user)
        else:
            fefs.likes.add(request.user) 
        return redirect('fefi:reply',fef_id=fef.id) 
@login_required
def edit(request):
    if request.method!='POST':
        profile_form=ProfileEditForm()
    else:
    
        profile_form=ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)
        if  profile_form.is_valid():
            profile_form.save()
            messages.success(request,'update succesfull')
            return redirect('fefi:edit')    
    return render(request,'fefi/edit.html',{'profile_form':profile_form})  
@login_required
def edit2(request):
    if request.method!='POST':
        user_form=UserEditForm()
    else:
        user_form=UserEditForm(instance=request.user,data=request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request,'update succesfull')
            return redirect('fefi:edit')    
    return render(request,'fefi/edit2.html',{'user_form':user_form,})  




    



 





       
      
    

  







         


  





  

            






   
     
  

       
