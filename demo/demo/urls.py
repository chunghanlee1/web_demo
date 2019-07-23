"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path, include
from demo import views, settings

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('^bbc_clone/$', include('bbc_clone.urls', namespace='bbc_clone')),
    re_path('^$', views.HomeTemplateView.as_view(), name='home'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('finance/', include('finance.urls', namespace='finance')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns=[re_path('^__debug__/', include(debug_toolbar.urls))]+urlpatterns
