from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class CloneTemplateView(TemplateView):
    template_name='bbc_clone/bbc_clone.html'