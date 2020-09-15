from django.shortcuts import render

# Create your views here.
def cars(request):
    context = {}
    template_name = 'cars/cars.html'
    return render(request, template_name, context)