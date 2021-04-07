from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from  .models import Post

# Create your views here.

@login_required(login_url='login')
def posts_list(request):
    queryset=Post.objects.all()
    context={
        'queryset': queryset,
    }
    return render(request,'testpostlists.html',context)