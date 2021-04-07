from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


from .decorators import unauthenicated_user

from  django.contrib import messages
# Create your views here.

#@login_required(login_url='login')

@unauthenicated_user
def login_page(request):

    if request.method=='POST':
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return HttpResponseRedirect('/posts/')
            # else:
            #     messages.info(request, 'Пароль или логин введены некорректно.')

    context={
    }
    return render(request,'testlogin.html',context)

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login/')
