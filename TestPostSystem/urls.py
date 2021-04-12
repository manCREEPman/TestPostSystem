"""TestPostSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from Tests.views import *
from Posts.views import *

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'main', main_page),
    url(r'create_test', create_test),
    url(r'create_tasks', create_tasks),
    url(r'user_unchecked_tests$', list_unchecked_user_tests),
    url(r'user_unchecked_tests/\d+$', check_user_test),

    url('login/', login_page, name='login' ),
    url('logout/',logout_user, name='logout'),
    url('posts/', posts_list, name='news' ),
    url('account/', account_page, name='account'),
    url('tests/', tests_page, name='tests'),
    url(r'pass_test/\d+$', pass_test),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

