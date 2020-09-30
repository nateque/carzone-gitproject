from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Car

# Create your views here.
def cars(request):
    cars = Car.objects.order_by('-created_date')
    paginator = Paginator(cars, 2)
    page = request.GET.get('page')
    paged_cars = paginator.get_page(page)

    model_search = Car.objects.values_list('model', flat=True).distinct()
    state_search = Car.objects.values_list('state', flat=True).distinct()
    year_search = Car.objects.values_list('year', flat=True).distinct()
    body_style_search = Car.objects.values_list('body_style', flat=True).distinct()

    context = {
        'cars':paged_cars,
        'model_search': model_search,
        'state_search': state_search,
        'year_search': year_search,
        'body_style_search': body_style_search,
    }
    template_name = 'cars/cars.html'
    return render(request, template_name, context)

def car_detail(request, id):
    car = get_object_or_404(Car, id=id)
    context = {
        'car':car,
    }
    template_name = 'cars/car_detail.html'
    return render(request, template_name, context)

def search(request):
    cars = Car.objects.order_by('-created_date')

    model_search = Car.objects.values_list('model', flat=True).distinct()
    state_search = Car.objects.values_list('state', flat=True).distinct()
    year_search = Car.objects.values_list('year', flat=True).distinct()
    body_style_search = Car.objects.values_list('body_style', flat=True).distinct()

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            cars = cars.filter(description__icontains=keyword)

    if 'model' in request.GET:
        model = request.GET['model']
        if model:
            cars = cars.filter(model__iexact=model)

    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            cars = cars.filter(state__iexact=state)

    if 'year' in request.GET:
        year = request.GET['year']
        if year:
            cars = cars.filter(year__iexact=year)

    if 'body_style' in request.GET:
        body_style = request.GET['body_style']
        if body_style:
            cars = cars.filter(body_style__iexact=body_style)

    if 'min_price' or 'max_price' in request.GET:
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        if min_price or max_price:
            cars = cars.filter(price__gte=min_price, price__lte=max_price)

    context = {
        'cars':cars,
        'model_search': model_search,
        'state_search': state_search,
        'year_search': year_search,
        'body_style_search': body_style_search,
    }
    template_name = 'cars/search.html'
    return render(request, template_name, context)