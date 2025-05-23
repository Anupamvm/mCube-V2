# Generated by Django 4.1.13 on 2024-11-16 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Holding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_symbol', models.CharField(blank=True, max_length=100, null=True)),
                ('average_price', models.FloatField(blank=True, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('exchange_segment', models.CharField(blank=True, max_length=50, null=True)),
                ('exchange_identifier', models.CharField(blank=True, max_length=50, null=True)),
                ('holding_cost', models.FloatField(blank=True, null=True)),
                ('market_value', models.FloatField(blank=True, null=True)),
                ('scrip_id', models.IntegerField(blank=True, null=True)),
                ('instrument_token', models.IntegerField(blank=True, null=True)),
                ('instrument_type', models.CharField(blank=True, max_length=50, null=True)),
                ('is_alternate_scrip', models.BooleanField(blank=True, null=True)),
                ('closing_price', models.FloatField(blank=True, null=True)),
                ('symbol', models.CharField(blank=True, max_length=100, null=True)),
                ('sellable_quantity', models.IntegerField(blank=True, null=True)),
                ('expiry_date', models.DateField(blank=True, null=True)),
                ('strike_price', models.FloatField(blank=True, null=True)),
                ('opt_type', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
    ]
