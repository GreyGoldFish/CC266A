from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:beer_id>/", views.beer_details, name="beer_details"),
    path('add_beer/', views.add_beer, name='add_beer'),
    path('update_beer/<int:beer_id>/', views.update_beer, name='update_beer'),
    path('delete_beer/<int:beer_id>/', views.delete_beer, name='delete_beer'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('search/', views.search_beers, name='search_beers'),
]