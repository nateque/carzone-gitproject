from django.shortcuts import render, redirect
from .models import Team
from cars.models import Car
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages

# Create your views here.
def home(request):
    teams = Team.objects.all()
    featured_cars = Car.objects.order_by('-created_date').filter(is_featured=True)
    all_cars = Car.objects.order_by('-created_date')
    # search_fields = Car.objects.values('model', 'state', 'body_style', 'year')
    model_search = Car.objects.values_list('model', flat=True).distinct()
    state_search = Car.objects.values_list('state', flat=True).distinct()
    year_search = Car.objects.values_list('year', flat=True).distinct()
    body_style_search = Car.objects.values_list('body_style', flat=True).distinct()
    
    context = {
        'teams':teams,
        'featured_cars': featured_cars,
        'all_cars': all_cars,
        'model_search': model_search,
        'state_search': state_search,
        'year_search': year_search,
        'body_style_search': body_style_search,
    }
    template_name = 'pages/home.html'
    return render(request, template_name, context)

def about(request):
    return render(request, 'pages/about.html')

def services(request):
    return render(request, 'pages/services.html')

def contact(request):

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        phone = request.POST['phone']
        message = request.POST['message']

        admin_mail = User.objects.get(is_superuser=True).email

        send_mail(
            subject,
            f'User Name: {name}, E-Mail: {email}, Phone: {phone}, Message: {message}',
            'itsnateque@gmail.com',
            [admin_mail],
        )

        messages.success(request, 'Your message has been submitted, we will get back to you shortly.')
        return redirect('contact')

    return render(request, 'pages/contact.html')
