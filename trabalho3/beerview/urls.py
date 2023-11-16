from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('beer_styles/', views.beer_styles, name='beer_styles'),
    path('beer_style/<int:beer_style_id>/', views.beer_style_details, name='beer_style_details'),
    path('breweries/', views.breweries, name='breweries'),
    path('brewery/<int:brewery_id>/', views.brewery_details, name='brewery_details'),
    path('brewery/search/', views.search_breweries, name='search_breweries'),
    path('brewery/add/', views.add_brewery, name='add_brewery'),
    path('beer/<int:beer_id>/', views.beer_details, name='beer_details'),
    path('beer/add/', views.add_beer, name='add_beer'),
    path('beer/update/<int:beer_id>/', views.update_beer, name='update_beer'),
    path('beer/delete/<int:beer_id>/', views.delete_beer, name='delete_beer'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('beer/search/', views.search_beers, name='search_beers'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
]