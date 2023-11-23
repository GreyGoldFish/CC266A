from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Beer, BeerStyle, Brewery, Review, Address
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

def beer_style_details(request, beer_style_id):
    beer_style = get_object_or_404(BeerStyle, pk=beer_style_id)
    beers = beer_style.beers.all()

    return render(request, 'beerview/beer_style_details.html', {'beer_style': beer_style, 'beers': beers})

def breweries(request):
    breweries = Brewery.objects.all()

    context = {
        "breweries": breweries,
    }

    return render(request, "beerview/breweries.html", context)

def search_breweries(request):
    query = request.GET.get('q')
    if query:
        breweries = Brewery.objects.filter(Q(name__icontains=query))
    else:
        breweries = Brewery.objects.all()
    return render(request, 'beerview/breweries.html', {'breweries': breweries})

def brewery_details(request, brewery_id):
    brewery = get_object_or_404(Brewery, pk=brewery_id)
    beers = brewery.beers.all()

    return render(request, 'beerview/brewery_details.html', {'brewery': brewery, 'beers': beers})

@login_required
def create_brewery(request):
    if request.method == "POST":
        form = BreweryForm(request.POST, request.FILES)
        if form.is_valid():
            address = Address(
                line1=form.cleaned_data['line1'],
                line2=form.cleaned_data['line2'],
                city=form.cleaned_data['city'],
                region=form.cleaned_data['region'],
                postal_code=form.cleaned_data['postal_code'],
                country=form.cleaned_data['country']
            )
            address.save()

            brewery = form.save(commit=False)
            brewery.address = address
            brewery.user = request.user
            brewery.save()

            return redirect('breweries')
    else:
        form = BreweryForm()
    return render(request, 'beerview/brewery_form.html', {'form': form})

@login_required
def update_brewery(request, brewery_id):
    brewery = get_object_or_404(Brewery, id=brewery_id)
    if request.method == "POST":
        form = BreweryForm(request.POST, instance=brewery)
        if form.is_valid():
            form.save()
            return redirect('brewery_details', brewery_id=brewery.id)
    else:
        form = BreweryForm(instance=brewery)
    return render(request, 'beerview/brewery_form.html', {'form': form, 'brewery': brewery})

@login_required
def delete_brewery(request, brewery_id):
    brewery = get_object_or_404(Brewery, id=brewery_id)

    if request.user == brewery.creator:
        brewery.delete()
        messages.success(request, "Brewery successfully deleted.")
    else:
        messages.error(request, "You do not have permission to delete this brewery.")

    return redirect('breweries')

def beer_details(request, beer_id):
    beer = get_object_or_404(Beer, pk=beer_id)
    reviews = beer.reviews.all()

    # As avaliações ficam na página de detalhes da cerveja
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.beer = beer
            review.user = request.user
            review.save()
            return redirect('beer_details', beer_id=beer.id)
    else:
        form = ReviewForm()

    return render(request, 'beerview/beer_details.html', {'beer': beer, 'reviews': reviews, 'form': form})

def search_beers(request):
    query = request.GET.get('q')
    if query:
        beers = Beer.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        beers = Beer.objects.all()
    return render(request, 'beerview/index.html', {'beers': beers})

@login_required
def create_beer(request):
    if request.method == "POST":
        form = BeerForm(request.POST, request.FILES)
        if form.is_valid():
            beer = form.save(commit=False)
            beer.user = request.user
            beer.save()
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

    if request.user == beer.user:
        beer.delete()
        messages.success(request, "Beer successfully deleted.")

    return redirect('index')

@login_required
def update_review(request, beer_id):
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
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.user == review.user:
        review.delete()
        messages.success(request, "Review successfully deleted.")
    else:
        messages.error(request, "You do not have permission to delete this review.")

    return redirect('beer_details', beer_id=review.beer.id)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})