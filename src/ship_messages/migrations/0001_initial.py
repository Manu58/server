# Generated by Django 4.2.5 on 2023-10-03 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ship1a2090',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('wind_spd', models.FloatField()),
                ('weather', models.CharField(max_length=30)),
                ('temp', models.FloatField()),
                ('pres', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ShipMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.TextField(max_length=20)),
                ('datetime', models.DateTimeField()),
                ('address_ip', models.GenericIPAddressField(protocol='ipv4')),
                ('address_port', models.PositiveIntegerField()),
                ('original_message_id', models.TextField(max_length=20)),
                ('status', models.CharField(choices=[('A', 'ok'), ('V', 'navigation receiver warning')], max_length=1)),
                ('lat', models.FloatField()),
                ('lat_dir', models.CharField(choices=[('N', 'North'), ('S', 'South')], max_length=1)),
                ('lon', models.FloatField()),
                ('lon_dir', models.CharField(choices=[('E', 'East'), ('W', 'West')], max_length=1)),
                ('spd_over_grnd', models.FloatField()),
                ('true_course', models.FloatField()),
                ('datestamp', models.PositiveIntegerField()),
                ('mag_variation', models.FloatField()),
                ('mag_var_dir', models.CharField(choices=[('E', 'East'), ('W', 'West')], max_length=1)),
            ],
            options={
                'ordering': ('device_id', 'datetime'),
            },
        ),
        migrations.CreateModel(
            name='WeatherStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timezone', models.CharField(max_length=20)),
                ('state_code', models.CharField(max_length=2)),
                ('country_code', models.CharField(max_length=3)),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('city_name', models.CharField(max_length=20)),
                ('station_id', models.CharField(max_length=12)),
                ('city_id', models.CharField(max_length=7)),
            ],
            options={
                'ordering': ('lat', 'lon'),
            },
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wind_spd', models.FloatField()),
                ('timestamp_utc', models.DateTimeField()),
                ('pres', models.FloatField()),
                ('weather', models.CharField(max_length=30)),
                ('temp', models.FloatField()),
                ('timestamp_local', models.DateTimeField()),
                ('weather_station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='measurements', to='ship_messages.weatherstation')),
            ],
        ),
    ]
