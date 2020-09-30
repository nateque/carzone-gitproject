from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail
from django.contrib.auth.models import User

# Create your views here.
def inquiry(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        car_id = request.POST['car_id']
        customer_need = request.POST['customer_need']
        car_title = request.POST['car_title']
        city = request.POST['city']
        state = request.POST['state']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']

        if request.user.is_authenticated:
            request_user_id = request.user.id
            has_contacted   = Contact.objects.all().filter(user_id=request_user_id, car_id=car_id)
            if has_contacted:
                messages.error(request, 'You have already made an inquiry.')
                return redirect('/cars/'+car_id)

        contact = Contact(first_name=first_name, last_name=last_name, car_id=car_id, customer_need=customer_need, 
        car_title=car_title, city=city, state=state, email=email, phone=phone, message=message, user_id=user_id)

        admin_mail = User.objects.get(is_superuser=True).email

        send_mail(
            f'Subject: {customer_need}',
            f'User Mail: {email} City: {city} State: {state} Car: {car_title} Message: {message}',
            'itsnateque@gmail.com',
            [admin_mail],
        )

        contact.save()
        messages.success(request, 'Your request has been submitted, we will get back to you shortly.')
        return redirect('/cars/'+car_id)
