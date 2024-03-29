from django.urls import path
from .views import *

urlpatterns = [
        path('upcoming-tours',UpcomingTour.as_view(),name='UpcomingTours'),
        path('ongoing-tours',OngoingTour.as_view(),name='OngoingTours'),
        path('ongoing-upcoming-tour',OngoingUpcomingTour.as_view(),name='on-going-up-coming'),
        path('my-booking-history',MyBookingHistory.as_view(),name='MyBookingHistory'),
        path('wishlist',WishListAPI.as_view(),name='WishList')
    ]
