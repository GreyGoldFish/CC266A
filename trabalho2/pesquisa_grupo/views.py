from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404
from .models import Integrante, Publicacao

def index(request):
    integrantes = Integrante.objects.all()
    return render(request, 'pesquisa_grupo/index.html', {'integrantes': integrantes})

def detalhes_integrante(request, integrante_id):
    integrante = get_object_or_404(Integrante, pk=integrante_id)
    publicacoes = integrante.publicacao_set.all()
    return render(request, 'pesquisa_grupo/detalhes_integrante.html', {'integrante': integrante, 'publicacoes': publicacoes})
