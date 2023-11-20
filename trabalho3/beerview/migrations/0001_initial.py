# Generated by Django 4.2.7 on 2023-11-20 13:55

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line1', models.CharField(max_length=255, verbose_name='address Line 1')),
                ('line2', models.CharField(blank=True, max_length=255, null=True, verbose_name='address Line 2')),
                ('city', models.CharField(max_length=255)),
                ('region', models.CharField(blank=True, max_length=255, null=True, verbose_name='state/Province/Region')),
                ('postal_code', models.CharField(max_length=12, validators=[django.core.validators.RegexValidator(message='The postal code must not have spaces', regex='^\\S+$')])),
                ('country', django_countries.fields.CountryField(max_length=2)),
            ],
            options={
                'verbose_name_plural': 'addresses',
            },
        ),
        migrations.CreateModel(
            name='Beer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('picture', models.ImageField(upload_to='beer_pictures/')),
                ('abv', models.DecimalField(decimal_places=1, help_text='Alcohol By Volume', max_digits=3, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='ABV')),
                ('ibu', models.PositiveIntegerField(blank=True, help_text='International Bitterness Units', null=True, verbose_name='IBU')),
                ('srm', models.PositiveIntegerField(blank=True, help_text='Standard Reference Method - color', null=True, verbose_name='SRM')),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='BeerStyle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField()),
                ('family', models.CharField(choices=[('BO', 'Bock'), ('BA', 'Brown Ale'), ('DA', 'Dark Ale'), ('DL', 'Dark Lager'), ('HY', 'Hybrid Beer'), ('IP', 'India Pale Ale'), ('PA', 'Pale Ale'), ('PL', 'Pale Lager'), ('PO', 'Porter'), ('SP', 'Specialty Beer'), ('ST', 'Stout'), ('SA', 'Strong Ale'), ('WH', 'Wheat Beer'), ('WS', 'Wild/Sour Beer')], max_length=2)),
                ('min_ibu', models.PositiveIntegerField(blank=True, help_text='Minimum International Bitterness Units', null=True)),
                ('max_ibu', models.PositiveIntegerField(blank=True, help_text='Maximum International Bitterness Units', null=True)),
                ('min_srm', models.PositiveIntegerField(blank=True, help_text='Minimum Standard Reference Method - color', null=True)),
                ('max_srm', models.PositiveIntegerField(blank=True, help_text='Maximum Standard Reference Method - color', null=True)),
                ('min_abv', models.DecimalField(blank=True, decimal_places=1, help_text='Minimum Alcohol By Volume', max_digits=3, null=True)),
                ('max_abv', models.DecimalField(blank=True, decimal_places=1, help_text='Maximum Alcohol By Volume', max_digits=3, null=True)),
                ('flavor_profile', models.TextField(blank=True)),
                ('history', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2, validators=[django.core.validators.MinValueValidator(Decimal('0.00')), django.core.validators.MaxValueValidator(Decimal('5.00'))])),
                ('comment', models.TextField()),
                ('beer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='beerview.beer')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Brewery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('picture', models.ImageField(upload_to='brewery_pictures/')),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='beerview.address')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'breweries',
            },
        ),
        migrations.AddField(
            model_name='beer',
            name='brewery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beers', to='beerview.brewery'),
        ),
        migrations.AddField(
            model_name='beer',
            name='style',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='beers', to='beerview.beerstyle'),
        ),
        migrations.AddField(
            model_name='beer',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
