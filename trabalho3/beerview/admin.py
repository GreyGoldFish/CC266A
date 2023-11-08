from django.contrib import admin
from .models import TipoEstilo, EstiloCerveja, Cerveja, Avaliacao, Endereco, Cervejaria

class AvaliacaoInline(admin.TabularInline):
    model = Avaliacao
    extra = 1  # Quantas linhas para adicionar avaliações serão mostradas

class CervejaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cervejaria', 'estilo', 'vol')  # Campos que aparecem na listagem
    list_filter = ('estilo', 'cervejaria')  # Filtros disponíveis na barra lateral
    search_fields = ('nome', 'cervejaria_nome')  # Campos pesquisáveis
    inlines = [AvaliacaoInline]

class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('cerveja', 'usuario', 'nota', 'comentario')
    list_filter = ('nota', 'usuario')
    search_fields = ('cerveja_nome', 'usuario_username')

admin.site.register(TipoEstilo)
admin.site.register(EstiloCerveja)
admin.site.register(Cerveja, CervejaAdmin)
admin.site.register(Avaliacao, AvaliacaoAdmin)
admin.site.register(Endereco)
admin.site.register(Cervejaria)
