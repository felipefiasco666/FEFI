from django.http import HttpResponse 
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm,UserRegistrationForm,UserEditForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method!='POST':
        form=UserRegistrationForm()
    else:
        form=UserRegistrationForm(data=request.POST)
        if form.is_valid():
            new_user=form.save()
            login(request,new_user)
            return redirect('fefi:index')
    return render(request,'registration/register.html',{'form':form})        



# Create your views here.
