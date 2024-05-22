import uuid
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import datetime
from .forms import UserSignupForm, airlineSignupForm, PassengerDetailsForm, EditProfileForm, CustomPasswordChangeForm
from .models import User, Airline, Route, AddAirline, PassengerDetails
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Route
from django.contrib import messages
from django.utils import timezone
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import random
import string

def airlinesignup(request):
    if request.method == 'POST':
        form = airlineSignupForm(request.POST, request.FILES)  # Handle files
        if form.is_valid():
            airline_name = form.cleaned_data['airlineName']
            airline_email = form.cleaned_data['airlineEmail']
            airline_phone = form.cleaned_data['airlinePhone']
            airline_password = form.cleaned_data['airlinePassword']
            airline_image = form.cleaned_data.get('airlineImage')  # Get image file

            airline = Airline.objects.create_user(
                email=airline_email, 
                name=airline_name, 
                phone=airline_phone, 
                password=airline_password, 
                image=airline_image,  # Save image
                is_staff=True
            )
            return redirect('airlinelogin')
        else:
            messages.error(request, 'Failed to authenticate user after signup.')
    else:
        form = airlineSignupForm()
    return render(request, 'airline/airlinesignup.html', {'form': form})


def usersignup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['userEmail']
            user_password = form.cleaned_data['userPassword']
            user_first_name = form.cleaned_data['userFname']
            user_last_name = form.cleaned_data['userLname']
            user_phone = form.cleaned_data['userPhone']
            
            user = User.objects.create_user(
                email=user_email,
                password=user_password,
                first_name=user_first_name,
                last_name=user_last_name,
                phone=user_phone
            )
            user = authenticate(request, email=user_email, password=user_password)
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('userlogin')
            else:
                messages.error(request, 'Failed to authenticate user after signup.')
    else:
        form = UserSignupForm()
    return render(request, 'user/usersignup.html', {'form': form})

def adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admindashboard')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, 'admin/adminlogin.html')

def airlinelogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        airline = authenticate(request, email=email, password=password)
        
        if airline is not None and airline.is_staff:
            login(request, airline)
            return redirect('airlinedashboard')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
    return render(request, 'airline/airlinelogin.html')


def userlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('userdashboard')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
    return render(request, 'user/userlogin.html')


def airlinedashboard(request):
    return render(request, 'airline/airlinedashboard.html')


def userdashboard(request):
    if request.user.is_authenticated:
        return render(request, 'user/userdashboard.html', {'user_id': request.user.id})
    else:
        return redirect('userlogin')

def userlogout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')


def index(request):
    return render(request, "index.html")


def airlinelist(request):
    if request.user.is_authenticated:
        airlines = Airline.objects.all()
        return render(request, 'admin/airlinelist.html', {'airlines': airlines})
    else:
        return redirect('adminlogin')

def userlist(request):
    if request.user.is_authenticated:
        users = User.objects.all()
        return render(request, 'admin/userlist.html', {'users': users})
    else:
        return redirect('adminlogin')


def route(request):
    if request.method == 'POST':
        start_location = request.POST['start_location']
        end_location = request.POST['end_location']
        
        # Check if the route already exists
        if Route.objects.filter(start_location=start_location, end_location=end_location).exists():
            messages.error(request, 'Route already exists.')
        else:
            route = Route.objects.create(start_location=start_location, end_location=end_location)
            route.save()
            messages.success(request, 'Route added successfully.')
            return redirect('routelist')  # Redirect to a view that displays a list of routes
    return render(request, 'admin/addroute.html')

def routelist(request):
    if request.user.is_authenticated:
        routes = Route.objects.all()
        return render(request, 'admin/routelist.html', {'routes': routes})
    else:
        return redirect('adminlogin')

def toggle_route_status(request, route_id):
    if request.method == 'POST':
        try:
            route = Route.objects.get(id=route_id)
            route.is_active = not route.is_active
            route.save()
            return JsonResponse({'status': 'success', 'is_active': route.is_active})
        except Route.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Route does not exist'})
    return JsonResponse({'status': 'fail', 'message': 'Invalid request method'})
    


@login_required(login_url='/airlinelogin/')
def addflightschedule(request):
    if not request.user.is_staff:
        return redirect('airlinelogin')

    airline = get_object_or_404(Airline, email=request.user.email)
    airline_name = airline.name
    airline_image = airline.image  # Get the airline image
    routes = Route.objects.filter(is_active=True)  # Filter only active routes
    now = timezone.now().strftime('%Y-%m-%dT%H:%M')
    
    if request.method == 'POST':
        flight_number = request.POST.get('flight_number')
        start_location = request.POST.get('start_location')
        end_location = request.POST.get('end_location')
        seats_capacity = request.POST.get('seats_capacity')
        departure_datetime_str = request.POST.get('departure_datetime')
        ticket_price = request.POST.get('ticket_price')
        
        departure_datetime = datetime.strptime(departure_datetime_str, '%Y-%m-%dT%H:%M')
        departure_datetime = timezone.make_aware(departure_datetime, timezone.get_current_timezone())
        
        if departure_datetime <= timezone.now():
            messages.error(request, "Departure datetime must be in the future.")
            return redirect('addflightschedule')
        
        new_flight = AddAirline(
            flight_number=flight_number,
            start_location=start_location,
            end_location=end_location,
            seats_capacity=seats_capacity,
            departure_datetime=departure_datetime,
            ticket_price=ticket_price,
            airline_name=airline_name,
            airline_image=airline_image,
        )
        new_flight.save()

        messages.success(request, "Airline added successfully!")
        return redirect('flightschedule')

    context = {
        'routes': routes,
        'min_date': now,
        'airline_name': airline_name,
        'airline_image': airline_image,
    }
    return render(request, 'airline/addflightschedule.html', context)


@login_required(login_url='/airlinelogin/')
def flightschedule(request):
    if not request.user.is_staff:
        return redirect('airlinelogin')
    schedules = AddAirline.objects.all()
    return render(request, 'airline/flightschedule.html', {'schedules': schedules})

from .forms import PassengerDetailsForm

def flightsearch(request):
    routes = Route.objects.all()
    if request.method == 'POST':
        flying_from = request.POST['flying_from']
        flying_to = request.POST['flying_to']
        departure_date = request.POST['departure_date']
        flight_type = request.POST['flight_type']
        adults = int(request.POST['adults'])
        children = int(request.POST['children'])

        total_passengers = adults + children

        if flight_type == 'one-way':
            flights = AddAirline.objects.filter(
                start_location=flying_from,
                end_location=flying_to,
                departure_datetime__date=departure_date
            )
            return render(request, 'user/flightsearchresult.html', {
                'flights': flights,
                'trip_type': 'one-way',
                'total_passengers': total_passengers
            })
        
        elif flight_type == 'roundtrip':
            return_date = request.POST['return_date']
            departing_flights = AddAirline.objects.filter(
                start_location=flying_from,
                end_location=flying_to,
                departure_datetime__date=departure_date
            )
            returning_flights = AddAirline.objects.filter(
                start_location=flying_to,
                end_location=flying_from,
                departure_datetime__date=return_date
            )
            return render(request, 'user/flightsearchresult.html', {
                'departing_flights': departing_flights,
                'returning_flights': returning_flights,
                'trip_type': 'roundtrip',
                'total_passengers': total_passengers
            })
    return render(request, 'user/flightsearch.html', {'routes': routes})

@login_required
def passenger_details(request):
    if request.method == 'POST':
        selected_flights = (
            request.POST.getlist('selected_flight') + 
            request.POST.getlist('selected_departing_flight') + 
            request.POST.getlist('selected_returning_flight')
        )
        total_passengers = int(request.POST.get('total_passengers', 0))
        passenger_forms = [PassengerDetailsForm(request.POST, prefix=str(i)) for i in range(total_passengers)]

        if 'submit' in request.POST:
            all_valid = all(form.is_valid() for form in passenger_forms)

            if all_valid:
                if selected_flights:
                    selected_flight = get_object_or_404(AddAirline, pk=selected_flights[0])
                    if selected_flight.seats_capacity < total_passengers:
                        messages.error(request, "Not enough available seats for this flight.")
                        return redirect('passenger_details')

                    # Generate a 6-character PNR
                    pnr = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                    booking = Booking(
                        booked_by=request.user,
                        departure_date=selected_flight.departure_datetime,
                        amount=selected_flight.ticket_price * total_passengers,
                        flight_number=selected_flight.flight_number,
                        airline_name=selected_flight.airline_name,
                        pnr=pnr,
                        number_of_passengers=total_passengers,
                        booked_date=timezone.now()  # Set the booking date
                    )
                    booking.save()

                    for form in passenger_forms:
                        passenger_detail = PassengerDetails(
                            first_name=form.cleaned_data['first_name'],
                            last_name=form.cleaned_data['last_name'],
                            email=form.cleaned_data['email'],
                            phone_number=form.cleaned_data['phone_number'],
                            passport_number=form.cleaned_data['passport_number'],
                            nationality=form.cleaned_data['nationality'],
                            flight=selected_flight,
                            booked_by=request.user,
                            booking=booking
                        )
                        passenger_detail.save()

                    selected_flight.seats_capacity -= total_passengers
                    selected_flight.save()

                    return redirect('make_payment', pnr=booking.pnr)
                else:
                    return render(request, 'user/passengerdetails.html', {
                        'passenger_forms': passenger_forms,
                        'total_passengers': total_passengers,
                        'error_message': 'No flights selected. Please select at least one flight.',
                        'selected_flights': selected_flights
                    })

        return render(request, 'user/passengerdetails.html', {
            'passenger_forms': passenger_forms,
            'total_passengers': total_passengers,
            'selected_flights': selected_flights
        })
    else:
        return redirect('flightsearch')
    

def bookingconfirmed(request):
    return render (request, 'user/bookingconfirmed.html')


@login_required
def user_bookings(request):
    user_bookings = Booking.objects.filter(booked_by=request.user)

    context = {
        'user': request.user,
        'user_bookings': user_bookings
    }
    return render(request, 'user/user_booking.html', context)

@login_required
def admin_bookings(request):
    all_bookings = PassengerDetails.objects.select_related('booked_by', 'flight').all()

    # Print debug information
    for booking in all_bookings:
        print(f"Booking ID: {booking.id}, Booked By: {booking.booked_by}, Booked By First Name: {booking.booked_by.first_name}")
    
    context = {
        'all_bookings': all_bookings,
    }
    return render(request, 'admin/admin_bookings.html', context)


@login_required
def airline_bookings(request):
    all_bookings = Booking.objects.select_related('booked_by').all()

    context = {
        'all_bookings': all_bookings,
    }
    return render(request, 'airline/airline_bookings.html', context)


@login_required
def user_details(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_bookings = PassengerDetails.objects.filter(booked_by=user)
    total_bookings = user_bookings.count()
    total_expenditure = sum(booking.flight.ticket_price for booking in user_bookings if booking.flight)

    data = {
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone': user.phone,
        'total_bookings': total_bookings,
        'total_expenditure': total_expenditure,
    }
    return JsonResponse(data)


def admindashboard(request):
    if request.user.is_authenticated:
        total_users = User.objects.count()
        total_airlines = Airline.objects.count()
        total_bookings = PassengerDetails.objects.count()
        total_upcoming_flights = AddAirline.objects.filter(departure_datetime__gte=timezone.now()).count()

        context = {
            'total_users': total_users,
            'total_airlines': total_airlines,
            'total_bookings': total_bookings,
            'total_upcoming_flights': total_upcoming_flights,
        }

        return render(request, 'admin/admindashboard.html', context)
    else:
        return redirect('adminlogin')



@login_required
def edituserdetails(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('userdashboard')
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'user/edit_user_details.html', {'form': form, 'user': user})


@login_required
def userpasswordreset(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to update the session with the new password
            messages.success(request, 'Your password was successfully updated!')
            return redirect('userdashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'user/userpasswordreset.html', {
        'form': form,
        'user': request.user
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Booking, AddAirline

def make_payment(request, pnr):
    booking = get_object_or_404(Booking, pnr=pnr)
    if request.method == 'POST':
        context = {"booking": booking}
        return render(request, 'user/make_payment.html', context)
    return render(request, 'user/make_payment.html', {'booking': booking})

def esewa_callback(request):
    pnr = request.GET.get('oid')
    amount = request.GET.get('amt')
    refId = request.GET.get('refId')

    try:
        booking = Booking.objects.get(pnr=pnr)
        if booking.amount == float(amount):
            booking.payment_status = True
            booking.save()

            # Reduce the number of available seats in the AddAirline model
            flight = AddAirline.objects.get(flight_number=booking.flight_number)
            flight.seats_capacity -= booking.number_of_passengers
            flight.save()

            return render(request, 'user/payment_success.html', {'booking': booking})
        else:
            return HttpResponse("Invalid Amount")
    except Booking.DoesNotExist:
        return HttpResponse("Booking Not Found")

def payment_failed(request):
    return HttpResponse("Payment Failed")

from django.views.decorators.http import require_http_methods
@login_required
@require_http_methods(["DELETE"])
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if not booking.payment_status and booking.booked_by == request.user:
        booking.delete()
        return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'status': 'failed'}, status=400)





@login_required
def download_ticket(request, pnr):
    try:
        booking = get_object_or_404(Booking, pnr=pnr)
        passengers = PassengerDetails.objects.filter(booking=booking)
        flight = get_object_or_404(AddAirline, flight_number=booking.flight_number)
        
        
        return_flight = None
        if 'return_flight_number' in booking.__dict__:
            return_flight = get_object_or_404(AddAirline, flight_number=booking.return_flight_number)

        # Create a file-like buffer to receive PDF data
        buffer = io.BytesIO()

        # Create the PDF object, using the buffer as its "file"
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Add airline image
        if flight.airline_image:
            airline_logo_full_path = flight.airline_image.path
            p.drawImage(ImageReader(airline_logo_full_path), 50, height - 100, width=200, height=50)

        # Add booking header details
        p.setFont("Helvetica-Bold", 7)
        p.drawString(50, height - 130, "THIS E-TICKET MUST BE PRESENTED DURING CHECK-INS. AT CHECK-IN PHASE PLEASE PRESENT ID CARD AND ALL NECESSARY TRAVEL DOCUMENTS.")
        
        # Add booking details
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, height - 160, "PASSENGER & TICKET INFORMATION")
        p.setFont("Helvetica", 12)
        y_position = height - 180
        for passenger in passengers:
            p.drawString(50, y_position, f"PASSENGER NAME: {passenger.first_name} {passenger.last_name}")
            y_position -= 20
        p.drawString(50, y_position, f"PNR NUMBER: {booking.pnr}")
        y_position -= 20
        p.drawString(50, y_position, f"ISSUED DATE: {booking.booked_date.strftime('%b %d, %Y')}")

        # Add flight information
        y_position -= 40
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y_position, "FLIGHT INFORMATION")
        p.setFont("Helvetica", 12)
        y_position -= 20
        p.drawString(50, y_position, f"FLIGHT NUMBER: {flight.flight_number}")
        y_position -= 20
        p.drawString(50, y_position, f"FROM: {flight.start_location}")
        y_position -= 20
        p.drawString(50, y_position, f"TO: {flight.end_location}")
        y_position -= 20
        p.drawString(50, y_position, f"FLIGHT DATE: {flight.departure_datetime.strftime('%b %d, %Y')}")
        y_position -= 20
        p.drawString(50, y_position, f"TIME: {flight.departure_datetime.strftime('%I:%M %p')}")
        
        if return_flight:
            # Add return flight information
            y_position -= 40
            p.setFont("Helvetica-Bold", 12)
            p.drawString(50, y_position, "RETURN FLIGHT INFORMATION")
            p.setFont("Helvetica", 12)
            y_position -= 20
            p.drawString(50, y_position, f"FLIGHT NUMBER: {return_flight.flight_number}")
            y_position -= 20
            p.drawString(50, y_position, f"FROM: {return_flight.start_location}")
            y_position -= 20
            p.drawString(50, y_position, f"TO: {return_flight.end_location}")
            y_position -= 20
            p.drawString(50, y_position, f"FLIGHT DATE: {return_flight.departure_datetime.strftime('%b %d, %Y')}")
            y_position -= 20
            p.drawString(50, y_position, f"TIME: {return_flight.departure_datetime.strftime('%I:%M %p')}")

        # Close the PDF object cleanly
        p.showPage()
        p.save()

        # Get the value of the BytesIO buffer and write it to the response
        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf', headers={'Content-Disposition': f'attachment; filename="ticket_{pnr}.pdf"'})

    except Booking.DoesNotExist:
        return HttpResponse("Booking Not Found")
    except AddAirline.DoesNotExist:
        return HttpResponse("Flight Not Found")
    except OSError as e:
        return HttpResponse(f"Error: {str(e)}")
