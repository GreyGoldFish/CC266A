from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django_countries.fields import CountryField
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from decimal import Decimal


class TipoEstilo(models.Model):
    nome = models.CharField(max_length=200, unique=True)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome

class EstiloCerveja(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="estilos")
    nome = models.CharField(max_length=200, unique=True)
    descricao = models.TextField()
    ibu_min = models.PositiveIntegerField(null=True, blank=True)
    ibu_max = models.PositiveIntegerField(null=True, blank=True)
    srm_min = models.PositiveIntegerField(null=True, blank=True)
    srm_max = models.PositiveIntegerField(null=True, blank=True)
    abv_min = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    abv_max = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    perfil_sabor = models.TextField(blank=True)
    historia = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nome} ({self.categoria.nome})"

class Cerveja(models.Model):
    nome = models.CharField(max_length=200)
    cervejaria = models.ForeignKey(Cervejaria, on_delete=models.CASCADE, related_name="cervejas")
    estilo = models.ForeignKey(EstiloCerveja, on_delete=models.SET_NULL, null=True, related_name="cervejas")
    abv = models.DecimalField(max_digits=4, decimal_places=2, help_text=_("Alcohol By Volume"))
    ibu = models.PositiveIntegerField(_("IBU"), null=True, blank=True, help_text=_("International Bitterness Units"))
    srm = models.PositiveIntegerField(_("SRM"), null=True, blank=True, help_text=_("Standard Reference Method - color"))
    descricao = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nome} - {self.estilo.nome}"

class Avaliacao(models.Model):
    cerveja = models.ForeignKey(Cerveja, on_delete=models.CASCADE, related_name="avaliacoes")
    usuario = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    nota = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('5.00'))])
    comentario = models.TextField()

    def __str__(self):
        return f"{self.usuario.username} - {self.nota} - {self.cerveja.nome}"

class Endereco(models.Model):
    linha1 = models.CharField(max_length=255, verbose_name="Endereço Linha 1")
    linha2 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Endereço Linha 2")
    cidade = models.CharField(max_length=255, verbose_name="Cidade")
    regiao = models.CharField(max_length=255, blank=True, null=True, verbose_name="Estado/Província/Região")
    codigo_postal = models.CharField(max_length=12, validators=[RegexValidator(regex=r'^\S+$', message="O código postal não deve conter espaços")], verbose_name="Código Postal")
    pais = CountryField(verbose_name="País")

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'

    def __str__(self):
        # Cria uma lista com os componentes do endereço que não estão vazios
        endereco_completo = filter(None, [self.linha1, self.linha2, self.cidade, self.regiao, self.codigo_postal, self.pais.name])
        # Junta os componentes com uma vírgula
        return ', '.join(endereco_completo)

class Cervejaria(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome da Cervejaria")
    endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE, verbose_name="Endereço")

    def __str__(self):
        return self.nome
    