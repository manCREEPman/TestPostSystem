from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect

def unauthenicated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/posts/')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func