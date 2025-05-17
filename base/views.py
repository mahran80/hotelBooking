from django.contrib.auth.models import User



from rest_framework import status
from django.contrib.auth import update_session_auth_hash
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from .models import Quiz
from .serializers import QuizSerializer, UserRegisterSerializer, UserSerializer,ChangePasswordSerializer

from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from room_booking.models import OccupiedDate
from django.utils.translation import gettext as _
import json


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.error)

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            tokens = response.data

            access_token = tokens['access']
            refresh_token = tokens['refresh']

            seriliazer = UserSerializer(request.user, many=False)

            res = Response()

            res.data = {'success':True}

            res.set_cookie(
                key='access_token',
                value=str(access_token),
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )

            res.set_cookie(
                key='refresh_token',
                value=str(refresh_token),
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )
            res.data.update(tokens)
            return res
        
        except Exception as e:
            print(e)
            return Response({'success':False})
        
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')

            request.data['refresh'] = refresh_token

            response = super().post(request, *args, **kwargs)
            
            tokens = response.data
            access_token = tokens['access']

            res = Response()

            res.data = {'refreshed': True}

            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,
                samesite='None',
                path='/'
            )
            return res

        except Exception as e:
            print(e)
            return Response({'refreshed': False})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):

    try:

        res = Response()
        res.data = {'success':True}
        res.delete_cookie('access_token', path='/', samesite='None')
        res.delete_cookie('response_token', path='/', samesite='None')

        return res

    except Exception as e:
        print(e)
        return Response({'success':False})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_Quiz(request):
    user = request.user
    quiz = Quiz.objects.filter(owner=user)
    serializer = QuizSerializer(quiz, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_logged_in(request):
    serializer = UserSerializer(request.user, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  # To update session after password change
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
@require_http_methods(["POST"])
def update_booking(request, booking_id):
    try:
        # Parse the request body
        data = json.loads(request.body)
        check_in = data.get('check_in')
        check_out = data.get('check_out')

        # Validate dates
        if not check_in or not check_out:
            return JsonResponse({'error': _('Both check-in and check-out dates are required')}, status=400)

        check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()

        if check_in_date >= check_out_date:
            return JsonResponse({'error': _('Check-out date must be after check-in date')}, status=400)

        # Get and update the booking
        booking = OccupiedDate.objects.get(id=booking_id, user=request.user)
        
        # Check if the dates are available
        conflicting_bookings = OccupiedDate.objects.filter(
            room=booking.room,
            date__range=[check_in_date, check_out_date]
        ).exclude(id=booking_id)
        
        if conflicting_bookings.exists():
            return JsonResponse({'error': _('These dates are not available')}, status=400)

        # Update the booking
        booking.date = check_in_date
        booking.checkout_date = check_out_date
        booking.save()

        return JsonResponse({'success': True})
    except OccupiedDate.DoesNotExist:
        return JsonResponse({'error': _('Booking not found')}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': _('Invalid request format')}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)