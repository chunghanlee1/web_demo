from django.views.generic import TemplateView
# Create your views here.

class HomeTemplateView(TemplateView):
    template_name='index.html'