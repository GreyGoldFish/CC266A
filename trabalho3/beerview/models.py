from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import RegexValidator
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from decimal import Decimal

class BeerStyle(models.Model):
    FAMILIES = [
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

    name = models.CharField(
        max_length=200,
        unique=True
    )
    description = models.TextField()
    family = models.CharField(
        max_length=2,
        choices=FAMILIES
    )
    min_ibu = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text=_("Minimum International Bitterness Units")
    )
    max_ibu = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text=_("Maximum International Bitterness Units")
    )
    min_srm = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text=_("Minimum Standard Reference Method - color")
    )
    max_srm = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text=_("Maximum Standard Reference Method - color")
    )
    min_abv = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        help_text=_("Minimum Alcohol By Volume"))
    max_abv = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        help_text=_("Maximum Alcohol By Volume")
    )
    flavor_profile = models.TextField(blank=True)
    history = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.family})"

class Address(models.Model):
    line1 = models.CharField(
        max_length=255,
        verbose_name="address Line 1"
    )
    line2 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="address Line 2"
    )
    city = models.CharField(max_length=255)
    region = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="state/Province/Region"
    )
    postal_code = models.CharField(
        max_length=12,
        validators=[
            RegexValidator(regex=r'^\S+$', message="The postal code must not have spaces")
        ]
    )
    country = CountryField()

    class Meta:
        verbose_name_plural = "addresses"

    def __str__(self):
        # Cria uma lista com os componentes do address que não estão vazios
        full_address = filter(
            None,
            [self.line1, self.line2, self.city, self.region, self.postal_code, self.country.name]
        )
        # Junta os componentes com uma vírgula
        return ', '.join(full_address)

class Brewery(models.Model):
    name = models.CharField(max_length=255)
    Address = models.OneToOneField(
        Address,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = "breweries"
    

    def __str__(self):
        return self.name

class Beer(models.Model):
    name = models.CharField(max_length=200)
    brewery = models.ForeignKey(
        Brewery,
        on_delete=models.CASCADE,
        related_name="beers"
    )
    style = models.ForeignKey(
        BeerStyle,
        on_delete=models.SET_NULL,
        null=True,
        related_name="beers"
    )
    abv = models.DecimalField(
        _("ABV"), max_digits=3,
        decimal_places=1,
        help_text=_("Alcohol By Volume"),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    ibu = models.PositiveIntegerField(
        _("IBU"),
        null=True,
        blank=True,
        help_text=_("International Bitterness Units")
    )
    srm = models.PositiveIntegerField(
        _("SRM"),
        null=True,
        blank=True,
        help_text=_("Standard Reference Method - color")
    )
    description = models.TextField(blank=True)

    def clean(self):
        beer_style = self.style

        if (beer_style.min_abv > self.abv or beer_style.max_abv < self.abv):
            raise ValidationError(
                f"ABV must be between {beer_style.min_abv} and {beer_style.max_abv} for it to be a {beer_style.name}."
            )
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.style.name}"

class Review(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    beer = models.ForeignKey(
        Beer,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True
    )
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1    ,
        validators=[
            MinValueValidator(Decimal('0.00')), 
            MaxValueValidator(Decimal('5.00'))
            ]
    )
    comment = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.rating} - {self.beer.name}"

    