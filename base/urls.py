from django.urls import path
from .views import (
    get_Quiz, CustomTokenObtainPairView, CustomTokenRefreshView, 
    register, is_logged_in, change_password, update_booking
)
from .frontend_views import logout_view

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', logout_view, name='logout'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('quiz/', get_Quiz),
    path('register/', register),
    path('authenticated/', is_logged_in),
    path('change_password/', change_password, name='change_password'),
    path('bookings/<int:booking_id>/update/', update_booking, name='update-booking'),
]