# Generated by Django 2.2 on 2021-02-27 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactmessage',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
