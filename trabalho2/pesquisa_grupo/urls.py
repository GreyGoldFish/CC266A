from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('integrantes/<int:integrante_id>/', views.detalhes_integrante, name='detalhes_integrante'),
]
