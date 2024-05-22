from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('usersignup/', views.usersignup, name="usersignup"),
    path('userlogin/', views.userlogin, name="userlogin"),
    path('userlogout/', views.userlogout, name="userlogout"),
    path('userdashboard/', views.userdashboard, name='userdashboard'),
    path('flightsearch/', views.flightsearch, name='flightsearch'),
    path('passengerdetails/', views.passenger_details, name='passenger_details'),
    path('bookingconfirmed/', views.bookingconfirmed, name='bookingconfirmed'),
    path('edituserdetails/<int:user_id>/', views.edituserdetails, name='edituserdetails'),
    path('userpasswordreset/', views.userpasswordreset, name='userpasswordreset'),

    path('airlinesignup/', views.airlinesignup, name="airlinesignup"),
    path('airlinelogin/', views.airlinelogin, name='airlinelogin'),
    path('airlinedashboard/', views.airlinedashboard, name='airlinedashboard'),
    path('flightschedule/', views.flightschedule, name='flightschedule'),
    path('addflightschedule/', views.addflightschedule, name='addflightschedule'),
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('admindashboard/', views.admindashboard, name='admindashboard'),
    path('airlinelist/', views.airlinelist, name='airlinelist'),
    path('userlist/', views.userlist, name='userlist'),
    path('addroute/', views.route, name='addroute'),
    path('routelist/', views.routelist, name='routelist'),
    path('toggle_status/<int:route_id>/', views.toggle_route_status, name='toggle_route_status'),
    path('userbooking/', views.user_bookings, name='user_bookings'),
    path('adminbooking/', views.admin_bookings, name='admin_bookings'),
    path('airlinebooking/', views.airline_bookings, name='airline_bookings'),
    path('userdetails/<int:user_id>/', views.user_details, name='user_details'),
    path('make-payment/<str:pnr>/', views.make_payment, name='make_payment'),
    path('esewa-callback/', views.esewa_callback, name='esewa_callback'),
    path('payment-failed/', views.payment_failed, name='payment_failed'),
    path('delete-booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('download-ticket/<str:pnr>/', views.download_ticket, name='download_ticket'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)