from django.urls import path
from . import views

urlpatterns = [
    # Module 1: User Management APIs
    path('users/add/', views.add_user, name='add_user'),
    path('users/', views.get_users, name='get_users'),
    path('users/update/<str:pk>/', views.update_user, name='update_user'),
    path('users/delete/<str:pk>/', views.delete_user, name='delete_user'),

    # Module 2: Event Management APIs
    path('events/add/', views.add_event, name='add_event'),
    path('events/', views.get_events, name='get_events'),
    path('events/update/<str:pk>/', views.update_event, name='update_event'),
    path('events/delete/<str:pk>/', views.delete_event, name='delete_event'),

    # Module 3: Venue Management APIs
    path('venues/add/', views.add_venue, name='add_venue'),
    path('venues/', views.get_venues, name='get_venues'),
    path('venues/update/<str:pk>/', views.update_venue, name='update_venue'),
    path('venues/delete/<str:pk>/', views.delete_venue, name='delete_venue'),

    # Module 4: Ticket Booking Management APIs
    path('bookings/add/', views.add_booking, name='add_booking'),
    path('bookings/', views.get_bookings, name='get_bookings'),
    path('bookings/update/<str:pk>/', views.update_booking, name='update_booking'),
    path('bookings/delete/<str:pk>/', views.delete_booking, name='delete_booking'),

    # Module 5: Payment Management APIs
    path('payments/add/', views.add_payment, name='add_payment'),
    path('payments/', views.get_payments, name='get_payments'),
    path('payments/update/<str:pk>/', views.update_payment, name='update_payment'),
    path('payments/delete/<str:pk>/', views.delete_payment, name='delete_payment'),
]
