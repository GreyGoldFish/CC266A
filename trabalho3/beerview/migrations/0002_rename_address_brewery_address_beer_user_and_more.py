# Generated by Django 4.2.7 on 2023-11-16 17:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('beerview', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='brewery',
            old_name='Address',
            new_name='address',
        ),
        migrations.AddField(
            model_name='beer',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='brewery',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='beerstyle',
            name='family',
            field=models.CharField(choices=[('BO', 'Bock'), ('BA', 'Brown Ale'), ('DA', 'Dark Ale'), ('HY', 'Hybrid Beer'), ('IP', 'India Pale Ale'), ('PA', 'Pale Ale'), ('PL', 'Pale Lager'), ('PO', 'Porter'), ('ES', 'Specialty Beer'), ('ST', 'Stout'), ('SA', 'Strong Ale'), ('WH', 'Wheat Beer'), ('WI', 'Wild/Sour Beer')], max_length=2),
        ),
    ]
