# Generated by Django 4.2 on 2024-05-21 16:19

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddAirline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_number', models.CharField(max_length=10)),
                ('start_location', models.CharField(max_length=100)),
                ('end_location', models.CharField(max_length=100)),
                ('seats_capacity', models.IntegerField()),
                ('departure_datetime', models.DateTimeField()),
                ('ticket_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('airline_name', models.CharField(max_length=100)),
                ('airline_image', models.ImageField(blank=True, null=True, upload_to='airline_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Airline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=True)),
                ('signup_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.ImageField(blank=True, null=True, upload_to='airline_images/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_date', models.DateTimeField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('flight_number', models.CharField(max_length=50)),
                ('airline_name', models.CharField(max_length=100)),
                ('pnr', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_location', models.CharField(max_length=100)),
                ('end_location', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('signup_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PassengerDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('passport_number', models.CharField(blank=True, max_length=50, null=True)),
                ('nationality', models.CharField(blank=True, max_length=50, null=True)),
                ('booked_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flightmandu.user')),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='passenger_details', to='flightmandu.booking')),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flightmandu.addairline')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='booked_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flightmandu.user'),
        ),
    ]