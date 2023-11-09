from django.contrib import admin
from .models import BeerStyle, Beer, Review, Address, Brewery

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1  # Quantas linhas para adicionar avaliações serão mostradas

class BeerAdmin(admin.ModelAdmin):
    list_display = ('name', 'brewery', 'style', 'abv')  # Campos que aparecem na listagem
    list_filter = ('style', 'brewery')  # Filtros disponíveis na barra lateral
    search_fields = ('name', 'brewery_name')  # Campos pesquisáveis
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
