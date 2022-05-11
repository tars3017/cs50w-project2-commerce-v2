# Generated by Django 4.0.3 on 2022-05-11 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_auction_list_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction_list',
            name='desc',
            field=models.CharField(default='description example', max_length=500),
        ),
        migrations.AlterField(
            model_name='auction_list',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]