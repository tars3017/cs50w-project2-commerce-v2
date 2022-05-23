# Generated by Django 4.0.3 on 2022-05-23 14:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_alter_bid_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_list',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='auction_list',
            name='current_bid',
            field=models.IntegerField(blank=True, default=''),
        ),
    ]
