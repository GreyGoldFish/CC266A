from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from decimal import Decimal

class EstiloCerveja(models.Model):
    FAMILIAS = [
        ('BO', 'Bock'),
        ('BA', 'Brown Ale'),
        ('DA', 'Dark Ale'),
        ('IP', 'Indian Pale Ale'),
        ('PA', 'Pale Ale'),
        ('PL', 'Pale Lager'),
        ('PO', 'Porter'),
        ('ES', 'Especial'),
        ('ST', 'Stout'),
        ('SA', 'Strong Ale'),
        ('WH', 'Wheat Beer'),
        ('WI', 'Wild Beer'),
    ]

    nome = models.CharField(max_length=200, unique=True)
    descricao = models.TextField()
    familia = models.CharField(max_length=2, choices=FAMILIAS)
    ibu_min = models.PositiveIntegerField(null=True, blank=True, help_text=_("Minimum International Bitterness Units"))
    ibu_max = models.PositiveIntegerField(null=True, blank=True, help_text=_("Maximum International Bitterness Units"))
    srm_min = models.PositiveIntegerField(null=True, blank=True, help_text=_("Minimum Standard Reference Method - color"))
    srm_max = models.PositiveIntegerField(null=True, blank=True, help_text=_("Maximum Standard Reference Method - color"))
    abv_min = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text=_("Minimum Alcohol By Volume"))
    abv_max = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text=_("Maximum Alcohol By Volume"))
    perfil_sabor = models.TextField(blank=True)
    historia = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nome} ({self.tipo.nome})"

class Endereco(models.Model):
    linha1 = models.CharField(max_length=255, verbose_name="endereço Linha 1")
    linha2 = models.CharField(max_length=255, blank=True, null=True, verbose_name="endereço Linha 2")
    cidade = models.CharField(max_length=255)
    regiao = models.CharField(max_length=255, blank=True, null=True, verbose_name="estado/Província/Região")
    codigo_postal = models.CharField(max_length=12, validators=[RegexValidator(regex=r'^\S+$', message="O código postal não deve conter espaços")], verbose_name="Código Postal")
    pais = CountryField(verbose_name="país")

    class Meta:
        verbose_name = 'endereço'
        verbose_name_plural = 'endereços'

    def __str__(self):
        # Cria uma lista com os componentes do endereço que não estão vazios
        endereco_completo = filter(None, [self.linha1, self.linha2, self.cidade, self.regiao, self.codigo_postal, self.pais.name])
        # Junta os componentes com uma vírgula
        return ', '.join(endereco_completo)

class Cervejaria(models.Model):
    nome = models.CharField(max_length=255)
    endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Cerveja(models.Model):
    nome = models.CharField(max_length=200)
    cervejaria = models.ForeignKey(Cervejaria, on_delete=models.CASCADE, related_name="cervejas")
    estilo = models.ForeignKey(EstiloCerveja, on_delete=models.SET_NULL, null=True, related_name="cervejas")
    abv = models.DecimalField(_("ABV"), max_digits=4, decimal_places=2, help_text=_("Alcohol By Volume"))
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

    class Meta:
        verbose_name = 'avaliação'
        verbose_name_plural = 'avaliações'

    def __str__(self):
        return f"{self.usuario.username} - {self.nota} - {self.cerveja.nome}"

    