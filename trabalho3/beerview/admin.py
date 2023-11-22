from django.contrib import admin
from .models import BeerStyle, Beer, Review, Address, Brewery

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

class BeerAdmin(admin.ModelAdmin):
    list_display = ('name', 'brewery', 'style', 'abv')
    list_filter = ('style', 'brewery')
    search_fields = ('name', 'brewery_name')
    inlines = [ReviewInline]

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('beer', 'user', 'rating', 'comment')
    list_filter = ('rating', 'user')
    search_fields = ('beer_name', 'user_name')

admin.site.register(BeerStyle)
admin.site.register(Beer, BeerAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Address)
admin.site.register(Brewery)
