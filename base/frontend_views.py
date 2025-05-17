from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from rest_framework_simplejwt.tokens import RefreshToken
from room_booking.models import Room, OccupiedDate, RoomImage
from .serializers import UserRegisterSerializer
from django.utils.translation import gettext as _
from datetime import datetime, timedelta
from django.db.models import Sum, Count, Q
from django.db import models

def register_view(request):
    if request.method == 'POST':
        serializer = UserRegisterSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.save()
            messages.success(request, _('Registration successful! Please login.'))
            return redirect('login')
        else:
            for error in serializer.errors.values():
                messages.error(request, error[0])
    return render(request, 'auth/register.html')

@csrf_protect
def login_view(request):
    # If user is already logged in, redirect to home
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Django session login
            login(request, user)
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            # Set response with tokens in cookies
            next_url = request.GET.get('next', 'home')
            response = redirect(next_url)
            response.set_cookie(
                'access_token',
                access_token,
                max_age=60*5,  # 5 minutes
                httponly=True,
                samesite='Lax',
                secure=False  # Set to True in production with HTTPS
            )
            response.set_cookie(
                'refresh_token',
                refresh_token,
                max_age=60*60*24,  # 1 day
                httponly=True,
                samesite='Lax',
                secure=False  # Set to True in production with HTTPS
            )
            
            return response
        else:
            messages.error(request, _('Invalid username or password.'))
    
    # Show login form for GET requests
    if request.GET.get('registered'):
        messages.success(request, _('Registration successful! Please login.'))
    return render(request, 'auth/login.html')

@csrf_protect
@require_http_methods(["POST"])
@login_required
def logout_view(request):
    # Clear session
    logout(request)
    
    # Clear auth cookies
    response = redirect('login')
    response.delete_cookie('access_token', path='/')
    response.delete_cookie('refresh_token', path='/')
    
    messages.success(request, _('You have been logged out successfully.'))
    return response

@login_required
def profile_view(request):
    # Get user's bookings
    user_bookings = OccupiedDate.objects.filter(user=request.user).select_related('room').order_by('-date')
    context = {
        'user': request.user,
        'bookings': user_bookings
    }
    return render(request, 'auth/profile.html', context)

def room_list_view(request):
    # Get filter parameters
    room_type = request.GET.get('type')
    max_occupancy = request.GET.get('maxOccupancy')
    min_price = request.GET.get('minPrice')
    max_price = request.GET.get('maxPrice')
    search = request.GET.get('search')
    
    # Start with all rooms
    rooms = Room.objects.all().prefetch_related('images')
    
    # Apply filters
    if room_type:
        rooms = rooms.filter(type=room_type)
    if max_occupancy:
        rooms = rooms.filter(maxOccupancy__gte=max_occupancy)
    if min_price:
        rooms = rooms.filter(pricePerNight__gte=min_price)
    if max_price:
        rooms = rooms.filter(pricePerNight__lte=max_price)
    if search:
        # Search in both name and description, case-insensitive
        rooms = rooms.filter(
            models.Q(name__icontains=search) |
            models.Q(description__icontains=search) |
            # Search in translated room types
            models.Q(type__in=[k for k, v in Room.ROOM_TYPES if _(v).lower().find(search.lower()) != -1])
        )
    
    context = {
        'rooms': rooms,
        'room_types': Room.ROOM_TYPES,
        'user': request.user,  # Explicitly add user to context
    }
    return render(request, 'room_booking/room_list.html', context)

def room_detail_view(request, pk):
    try:
        room = Room.objects.prefetch_related('images').get(pk=pk)
        # Get room's occupied dates
        occupied_dates = OccupiedDate.objects.filter(room=room).values_list('date', flat=True)
        
        context = {
            'room': room,
            'occupied_dates': list(occupied_dates),
            'today': datetime.now().date()  # Add today's date for date input min
        }
        return render(request, 'room_booking/room_detail.html', context)
    except Room.DoesNotExist:
        messages.error(request, _('Room not found.'))
        return redirect('room-list')

@login_required
def book_room(request, pk):
    if request.method != 'POST':
        messages.error(request, _('Invalid request method.'))
        return redirect('room-detail', pk=pk)

    try:
        room = Room.objects.get(pk=pk)
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')

        # Validate dates and availability here
        # Create booking
        booking = OccupiedDate.objects.create(
            room=room,
            user=request.user,
            date=check_in
        )
        
        messages.success(request, _('Room booked successfully!'))
        return redirect('room-detail', pk=pk)
    except Room.DoesNotExist:
        messages.error(request, _('Room not found.'))
        return redirect('room-list')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('room-detail', pk=pk)

@login_required
def cancel_booking(request, booking_id):
    try:
        booking = OccupiedDate.objects.get(id=booking_id, user=request.user)
        booking.delete()
        messages.success(request, _('Booking cancelled successfully.'))
    except OccupiedDate.DoesNotExist:
        messages.error(request, _('Booking not found.'))
    
    return redirect('profile') 