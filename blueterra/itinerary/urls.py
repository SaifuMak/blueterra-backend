
from django.urls import path,include

from .views import *

urlpatterns = [
   path('create-itinerary/', ItineraryCreateAPIView.as_view(), name='create_itinerary'),
   path("itineraries/", ItineraryListAPIView.as_view(), name="itinerary-list"),
   path('itinerary/<int:pk>/', ItineraryDetailView.as_view(), name='itinerary_details'),
   path('itinerary-list/', itinerary_list, name='itinerary-list'),
   path('itinerary-details/<int:pk>/', itinerary_detail, name='itinerary_details_for_user'),

]
