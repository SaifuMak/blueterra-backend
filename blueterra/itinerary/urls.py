
from django.urls import path,include

from .views import *

urlpatterns = [
   path('create-itinerary/', ItineraryCreateAPIView.as_view(), name='create_itinerary'),
   path("itineraries/", ItineraryListAPIView.as_view(), name="itinerary-list"),
   path('itinerary/<int:pk>/', ItineraryDetailView.as_view(), name='itinerary_details'),
   path('itinerary-list/', itinerary_list, name='itinerary-list'),
   path('itinerary-details/<int:pk>/', itinerary_detail, name='itinerary_details_for_user'),

   path("collections/", CollectionsAdminAPIView.as_view(), name="collection-list"),
   path("collections/<int:pk>/", CollectionsAdminAPIView.as_view(), name="collection"),

   path("destinations/", DestinationsAdminAPIView.as_view(), name="destinations-list"),
   path("destinations/<int:pk>/", DestinationsAdminAPIView.as_view(), name="destination"),

   path("destinations-list/", destination_list, name="destination_list"),

   path("countries/", CountriesAdminAPIView.as_view(), name="countries"),
   path("country/<int:pk>/", CountriesAdminAPIView.as_view(), name="country"),



]
