# Generated by Django 4.0.6 on 2022-08-04 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_shop', '0002_alter_category_options_product_product_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
