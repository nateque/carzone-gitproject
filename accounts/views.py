from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact
from django.contrib.auth.decorators import login_required

# Create your views here.
def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    template_name = 'accounts/login.html'
    context = {}
    return render(request, template_name, context)

def register(request):

    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('register')
            
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists')
                    return redirect('register')

                else:
                    user = User.objects.create_user(first_name=firstname, last_name=lastname, username=username, email=email, password=password)
                    auth.login(request, user)
                    messages.success(request, 'You are now logged in')
                    return redirect('dashboard')
                    user.save()
                    messages.success(request, 'You are now registered')
                    return redirect('login')

        else:
            messages.error(request, 'Password did not matched')
            return redirect('register')

    template_name = 'accounts/register.html'
    context = {}
    return render(request, template_name, context)


def logout(request):
    
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are successfully logged out.')
        return redirect('login')

    return redirect('home')

@login_required(login_url= 'login')
def dashboard(request):
    inquiries = Contact.objects.order_by('create_date').filter(user_id=request.user.id)
    template_name = 'accounts/dashboard.html'
    context = {
        'inquiries': inquiries,
    }
    return render(request, template_name, context)