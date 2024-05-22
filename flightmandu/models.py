from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
#Custom User Model
class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    signup_timestamp = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    def __str__(self):
        return self.email
    
#Custom Airline Model
class Airline(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    signup_timestamp = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='airline_images/', blank=True, null=True)  # New image field
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    def __str__(self):
        return self.email
    
class Route(models.Model):
    start_location = models.CharField(max_length=100)
    end_location = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.start_location} to {self.end_location}"

class AddAirline(models.Model):
    flight_number = models.CharField(max_length=10)
    start_location = models.CharField(max_length=100)
    end_location = models.CharField(max_length=100)
    seats_capacity = models.IntegerField()
    departure_datetime = models.DateTimeField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    airline_name = models.CharField(max_length=100)
    airline_image = models.ImageField(upload_to='airline_images/', blank=True, null=True)

    def __str__(self):
        return f"Flight {self.flight_number}: {self.start_location} to {self.end_location}"

class Booking(models.Model):
    booked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    departure_date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    flight_number = models.CharField(max_length=50)
    airline_name = models.CharField(max_length=100)
    pnr = models.CharField(max_length=6, unique=True)
    payment_status = models.BooleanField(default=False)
    number_of_passengers = models.IntegerField()
    booked_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Booking {self.pnr} by {self.booked_by.username}"

class PassengerDetails(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    passport_number = models.CharField(max_length=50, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    flight = models.ForeignKey(AddAirline, on_delete=models.CASCADE)
    booked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='passenger_details')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.booking.pnr}"