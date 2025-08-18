
from django.urls import path,include

from .views import *

urlpatterns = [
   path('create-itinerary/', ItineraryCreateAPIView.as_view(), name='create_itinerary'),
    path("itineraries/", ItineraryListAPIView.as_view(), name="itinerary-list"),
]
