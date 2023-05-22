# Generated by Django 4.2 on 2023-05-22 01:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estabelecimento', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='estabelecimento',
            name='limite_maximo',
            field=models.DecimalField(decimal_places=2, default=70, max_digits=4, validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
