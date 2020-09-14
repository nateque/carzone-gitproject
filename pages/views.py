from django.shortcuts import render
from .models import Team

# Create your views here.
def home(request):
    teams = Team.objects.all()
    
    context = {
        'teams':teams,
    }
    template_name = 'pages/home.html'
    return render(request, template_name, context)

def about(request):
    return render(request, 'pages/about.html')

def services(request):
    return render(request, 'pages/services.html')

def contact(request):
    return render(request, 'pages/contact.html')
