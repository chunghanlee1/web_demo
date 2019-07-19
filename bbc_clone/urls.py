from django.contrib import admin
from django.urls import path, re_path
from bbc_clone import views
from django.urls import path, re_path

app_name='bbc_clone'

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', views.CloneTemplateView.as_view(), name='clone')
]
