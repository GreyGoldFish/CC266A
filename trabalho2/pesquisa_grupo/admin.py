from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Integrante, Publicacao

admin.site.register(Integrante)
admin.site.register(Publicacao)
