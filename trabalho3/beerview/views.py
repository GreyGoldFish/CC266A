from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Beer, BeerStyle, Brewery, Review
from .forms import ReviewForm, BeerForm, BreweryForm, RegisterForm

def index(request):
    beers = Beer.objects.all()

    context = {
        "beers": beers,
    }

    return render(request, "beerview/index.html", context)

def beer_styles(request):
    beer_styles = BeerStyle.objects.all()

    context = {
        "beer_styles": beer_styles,
    }

    return render(request, "beerview/beer_styles.html", context)

def breweries(request):
    breweries = Brewery.objects.all()

    context = {
        "breweries": breweries,
    }

    return render(request, "beerview/breweries.html", context)

def search_breweries(request):
    query = request.GET.get('q')
    if query:
        breweries = Brewery.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        breweries = Brewery.objects.all()
    return render(request, 'beerview/brewery.html', {'breweries': breweries})

def brewery_details(request, brewery_id):
    brewery = get_object_or_404(Brewery, pk=brewery_id)
    beers = brewery.beers.all()

    return render(request, 'beerview/brewery_details.html', {'brewery': brewery, 'beers': beers})

@login_required
def add_brewery(request):
    if request.method == "POST":
        form = BreweryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('breweries')
    else:
        form = BreweryForm()
    return render(request, 'beerview/brewery_form.html', {'form': form})

def beer_styles(request):
    beer_styles = BeerStyle.objects.all()

    context = {
        "beer_styles": beer_styles,
    }

    return render(request, "beerview/beer_styles.html", context)

def beer_style_details(request, beer_style_id):
    beer_style = get_object_or_404(BeerStyle, pk=beer_style_id)
    beers = beer_style.beers.all()

    return render(request, 'beerview/beer_style_details.html', {'beer_style': beer_style, 'beers': beers})

def search_beers(request):
    query = request.GET.get('q')
    if query:
        beers = Beer.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        beers = Beer.objects.all()
    return render(request, 'beerview/index.html', {'beers': beers})

def beer_details(request, beer_id):
    beer = get_object_or_404(Beer, pk=beer_id)
    reviews = beer.reviews.all()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.beer = beer
            review.user = request.user  # Assuming the user is authenticated
            review.save()
            return redirect('beer_details', beer_id=beer.id)
    else:
        form = ReviewForm()

    return render(request, 'beerview/beer_details.html', {'beer': beer, 'reviews': reviews, 'form': form})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    beer_id = review.beer.id
    review.delete()
    return redirect('beer_details', beer_id=beer_id)

@login_required
def add_beer(request):
    if request.method == "POST":
        form = BeerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = BeerForm()
    return render(request, 'beerview/beer_form.html', {'form': form})

@login_required
def update_beer(request, beer_id):
    beer = get_object_or_404(Beer, id=beer_id)
    if request.method == "POST":
        form = BeerForm(request.POST, instance=beer)
        if form.is_valid():
            form.save()
            return redirect('beer_details', beer_id=beer.id)
    else:
        form = BeerForm(instance=beer)
    return render(request, 'beerview/beer_form.html', {'form': form, 'beer': beer})

@login_required
def delete_beer(request, beer_id):
    beer = get_object_or_404(Beer, id=beer_id)
    beer.delete()
    return redirect('index')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})