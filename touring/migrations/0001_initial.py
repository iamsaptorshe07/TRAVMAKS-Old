# Generated by Django 2.2 on 2020-12-31 10:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('travelagency', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=255, unique=True)),
                ('customer_name', models.CharField(max_length=500)),
                ('customer_email', models.EmailField(max_length=254)),
                ('customer_phone', models.CharField(max_length=15)),
                ('customer_address', models.CharField(max_length=600)),
                ('total_people', models.IntegerField()),
                ('paid_by_user', models.FloatField()),
                ('total_price', models.FloatField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=False)),
                ('agent_approval', models.BooleanField(default=False)),
                ('user_cancel', models.BooleanField(default=False)),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Agency', to='accounts.AgencyDetail')),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Agent', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL)),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Tour', to='travelagency.Tour')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(default='test', max_length=255, unique=True)),
                ('banktransaction_id', models.CharField(default='test', max_length=255, unique=True)),
                ('txn_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('gateway_name', models.CharField(default='test', max_length=100)),
                ('bankname', models.CharField(default='test', max_length=200)),
                ('payment_mode', models.CharField(default='test', max_length=200)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('Order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Order', to='touring.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Failed_Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=255, unique=True)),
                ('customer_name', models.CharField(max_length=500)),
                ('customer_email', models.EmailField(max_length=254)),
                ('customer_phone', models.CharField(max_length=15)),
                ('customer_address', models.CharField(max_length=600)),
                ('total_people', models.IntegerField()),
                ('paid_by_user', models.FloatField()),
                ('total_price', models.FloatField()),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='FAgency', to='accounts.AgencyDetail')),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='FAgent', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Fcustomer', to=settings.AUTH_USER_MODEL)),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='FTour', to='travelagency.Tour')),
            ],
        ),
        migrations.CreateModel(
            name='Cancelled_Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=255, unique=True)),
                ('customer_name', models.CharField(max_length=500)),
                ('customer_email', models.EmailField(max_length=254)),
                ('customer_phone', models.CharField(max_length=15)),
                ('customer_address', models.CharField(max_length=600)),
                ('total_people', models.IntegerField()),
                ('paid_by_user', models.FloatField()),
                ('total_price', models.FloatField()),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('cancelled_by', models.CharField(choices=[('AGENT', 'AGENT'), ('USER', 'USER')], max_length=200)),
                ('cancel_reason', models.TextField(blank=True, null=True)),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CAgency', to='accounts.AgencyDetail')),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CAgent', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Ccustomer', to=settings.AUTH_USER_MODEL)),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CTour', to='travelagency.Tour')),
            ],
        ),
    ]