# Generated by Django 2.2 on 2021-02-22 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_guideservice_guideservicearea'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgencyRequestCallBack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('agencyName', models.CharField(max_length=200)),
                ('message', models.TextField()),
            ],
        ),
    ]