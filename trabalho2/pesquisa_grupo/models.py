from django.db import models

# Create your models here.

class Integrante(models.Model):
    TIPOS = [
        ('IC', 'Iniciação Científica'),
        ('ME', 'Mestrando'),
        ('DO', 'Doutorando'),
        ('PD', 'Pós-Doutorando'),
        ('PR', 'Professor'),
    ]
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=2, choices=TIPOS)
    foto = models.ImageField(upload_to='fotos_integrantes/', blank=True, null=True)

    def __str__(self):
        return self.nome

class Publicacao(models.Model):
    titulo = models.CharField(max_length=200)
    ano_publicacao = models.IntegerField()
    veiculo_publicacao = models.CharField(max_length=200)
    autores = models.ManyToManyField(Integrante)

    def __str__(self):
        return f"{self.titulo} ({self.ano_publicacao})"