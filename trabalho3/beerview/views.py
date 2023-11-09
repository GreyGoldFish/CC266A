from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q

from .models import Beer, Review
from .forms import ReviewForm, BeerForm

def index(request):
    beers = Beer.objects.all()

    context = {
        "beers": beers,
    }

    return render(request, "beerview/index.html", context)


def beer_details(request, beer_id):
    beer = get_object_or_404(Beer, pk=beer_id)
    reviews = beer.reviews.all()
    return render(request, 'beerview/beer_details.html', {'beer': beer, 'reviews': reviews})

def add_review(request, beer_id):
    beer = get_object_or_404(Beer, id=beer_id)
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
    return render(request, 'beerview/add_review.html', {'form': form, 'beer': beer})

def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    beer_id = review.beer.id
    review.delete()
    return redirect('beer_details', beer_id=beer_id)

def search_beers(request):
    query = request.GET.get('q')
    if query:
        beers = Beer.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        beers = Beer.objects.all()
    return render(request, 'beerview/index.html', {'beers': beers})

def add_beer(request):
    if request.method == "POST":
        form = BeerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = BeerForm()
    return render(request, 'beerview/add_beer.html', {'form': form})

def update_beer(request, beer_id):
    beer = get_object_or_404(Beer, id=beer_id)
    if request.method == "POST":
        form = BeerForm(request.POST, instance=beer)
        if form.is_valid():
            form.save()
            return redirect('beer_details', beer_id=beer.id)
    else:
        form = BeerForm(instance=beer)
    return render(request, 'beerview/update_beer.html', {'form': form, 'beer': beer})

def delete_beer(request, beer_id):
    beer = get_object_or_404(Beer, id=beer_id)
    beer.delete()
    return redirect('index')