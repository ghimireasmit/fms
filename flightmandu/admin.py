from django.contrib import admin
from .models import User, Airline, Route, AddAirline, PassengerDetails, Booking

admin.site.register(User)
admin.site.register(Airline)
admin.site.register(Route)
admin.site.register(AddAirline)
admin.site.register(PassengerDetails)
admin.site.register(Booking)