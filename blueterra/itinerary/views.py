from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import *
import json
from  .serializers import ItineraryListSerializer, ItineraryDetailsSerializer, ItineraryUserListingSerializer,UserItineraryDetailsSerializer,CollectionsListSerializer,DestinationsListSerializer,CountriesListSerializer
from  journals.paginations import GeneralPagination
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view


class ItineraryCreateAPIView(APIView):

    @transaction.atomic
    def post(self, request):
        try:
            is_published_str = request.data.getlist("is_published")

            if is_published_str:
                is_published_str = is_published_str[0]  # take first value

            is_published = str(is_published_str).lower() in ["true", "1", "yes"]


            # Main Itinerary
            itinerary = Itinerary.objects.create(
                title=request.data.get("title"),
                location_title=request.data.get("location_title"),
                description=request.data.get("description"),
                color=request.data.get("color"),
                destination=request.data.get("destination"),
                country=request.data.get("country"),
                collection=request.data.get("collection"),
                category=request.data.get("category"),
                banner_image=request.FILES.get("banner_image"),
                is_published = is_published,
            )

            # Destination Highlights
            destination_highlights = json.loads(request.data.get("destination_highlights", "[]"))
            for item in destination_highlights:
                DestinationHighlight.objects.create(itinerary=itinerary, title=item.get("title"))

            # Signature Highlights
            signature_highlights = json.loads(request.data.get("signature_highlights", "[]"))
            for item in signature_highlights:
                SignatureHighlight.objects.create(itinerary=itinerary, title=item.get("title"))

            # Package Inclusions
            package_inclusions = json.loads(request.data.get("package_inclusions", "[]"))
            for item in package_inclusions:
                PackageInclusion.objects.create(itinerary=itinerary, title=item.get("title"))

            # Package Exclusions
            package_exclusions = json.loads(request.data.get("package_exclusions", "[]"))
            for item in package_exclusions:
                PackageExclusion.objects.create(itinerary=itinerary, title=item.get("title"))

            # Map Routing
            map_routing = json.loads(request.data.get("map_routing", "[]"))
            for item in map_routing:
                MapRouting.objects.create(
                    itinerary=itinerary,
                    location=item.get("location"),
                    coordinates=item.get("coordinates"),
                    transfer=item.get("transfer", "Land"),
                )

            # Featured Points
            featured_points = json.loads(request.data.get("featured_points", "[]"))
            for item in featured_points:
                FeaturedPoint.objects.create(
                    itinerary=itinerary,
                    suggested_date=item.get("suggestedDate"),
                    price=item.get("price"),
                    additional_information=item.get("additionalInformation"),
                )

            # Days (with image files)
            index = 0
            while f"days[{index}][title]" in request.data:
                Day.objects.create(
                    itinerary=itinerary,
                    title=request.data.get(f"days[{index}][title]"),
                    description=request.data.get(f"days[{index}][description]"),
                    image=request.FILES.get(f"days[{index}][image]"),
                    image_title=request.data.get(f"days[{index}][image_title]"),
                    order = index
                )
                index += 1

            # Hotels (with image files)
            index = 0
            while f"hotels[{index}][title]" in request.data:
                Hotel.objects.create(
                    itinerary=itinerary,
                    title=request.data.get(f"hotels[{index}][title]"),
                    description=request.data.get(f"hotels[{index}][description]"),
                    image=request.FILES.get(f"hotels[{index}][image]"),
                    coordinates=request.data.get(f"hotels[{index}][coordinates]"),
                    location=request.data.get(f"hotels[{index}][location]"),
                    map_link=request.data.get(f"hotels[{index}][mapLink]"),
                    rating=request.data.get(f"hotels[{index}][rating]") or 5,
                    order = index
                )
                index += 1

            # Gallery (image + title)
            index = 0
            while f"gallery[{index}][image]" in request.FILES or f"gallery[{index}][title]" in request.data:
                Gallery.objects.create(
                    itinerary=itinerary,
                    image=request.FILES.get(f"gallery[{index}][image]"),
                    title=request.data.get(f"gallery[{index}][title]"),
                )
                index += 1

            return Response({"message": "Itinerary created successfully!"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            transaction.set_rollback(True)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ItineraryListAPIView(APIView):
    def get(self, request):
        status_param = request.query_params.get('status')
        
        itineraries = Itinerary.objects.all().order_by('-created_at')

        if status_param == 'Published':
            itineraries = itineraries.filter(is_published=True)
        else:
            itineraries = itineraries.filter(is_published=False)

        paginator = GeneralPagination()
        result_page = paginator.paginate_queryset(itineraries, request)

        serializer = ItineraryListSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    

    def patch(self, request):
        itinerary_id = request.data.get("id")
        if not itinerary_id:
            return Response({"error": "Itinerary is not selected."}, status=status.HTTP_400_BAD_REQUEST)

        itinerary = get_object_or_404(Itinerary, pk=itinerary_id)

        # If only is_published is being updated
        if "status" in request.data and len(request.data) == 2:
            if  request.data["status"] == 'publish':
                itinerary.is_published = True
            else:
                itinerary.is_published =  False
            itinerary.save()
            return Response({"message": "Publish status updated successfully."}, status=status.HTTP_200_OK)
        



class ItineraryDetailView(APIView):

    def get(self, request, pk):

        try:
            itinerary = get_object_or_404(Itinerary, pk=pk)
            serializer = ItineraryDetailsSerializer(itinerary)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))

    
    def delete(self, request, pk):
        itinerary = get_object_or_404(Itinerary, pk=pk)
        itinerary.delete()
        return Response({"message": "Journal deleted successfully"}, status=status.HTTP_200_OK)

    
    @transaction.atomic
    def patch(self, request, pk):
        try:
            itinerary = get_object_or_404(Itinerary, pk=pk)

            # Update simple fields
            itinerary.title = request.data.get("title", itinerary.title)
            itinerary.location_title = request.data.get("location_title", itinerary.location_title)
            itinerary.description = request.data.get("description", itinerary.description)
            itinerary.color = request.data.get("color", itinerary.color)
            itinerary.destination = request.data.get("destination", itinerary.destination)
            itinerary.country = request.data.get("country", itinerary.country)
            itinerary.collection = request.data.get("collection", itinerary.collection)
            itinerary.category = request.data.get("category", itinerary.category)

            # Banner image: replace only if new file uploaded
            if "banner_image" in request.FILES:
                itinerary.banner_image = request.FILES["banner_image"]

            itinerary.save()

             # Destination Highlights
            DestinationHighlight.objects.filter(itinerary=itinerary).delete()
            destination_highlights = json.loads(request.data.get("destination_highlights", "[]"))
            for item in destination_highlights:
                DestinationHighlight.objects.create(itinerary=itinerary, title=item.get("title"))

            # Signature Highlights
            SignatureHighlight.objects.filter(itinerary=itinerary).delete()
            signature_highlights = json.loads(request.data.get("signature_highlights", "[]"))
            for item in signature_highlights:
                SignatureHighlight.objects.create(itinerary=itinerary, title=item.get("title"))

            # Package Inclusions
            PackageInclusion.objects.filter(itinerary=itinerary).delete()
            package_inclusions = json.loads(request.data.get("package_inclusions", "[]"))
            for item in package_inclusions:
                PackageInclusion.objects.create(itinerary=itinerary, title=item.get("title"))

            # Package Exclusions
            PackageExclusion.objects.filter(itinerary=itinerary).delete()
            package_exclusions = json.loads(request.data.get("package_exclusions", "[]"))
            for item in package_exclusions:
                PackageExclusion.objects.create(itinerary=itinerary, title=item.get("title"))

            # Map Routing
            MapRouting.objects.filter(itinerary=itinerary).delete()
            map_routing = json.loads(request.data.get("map_routing", "[]"))
            for item in map_routing:
                MapRouting.objects.create(
                    itinerary=itinerary,
                    location=item.get("location"),
                    coordinates=item.get("coordinates"),
                    transfer=item.get("transfer", "Land"),
                )

            # Featured Points
            FeaturedPoint.objects.filter(itinerary=itinerary).delete()
            featured_points = json.loads(request.data.get("featured_points", "[]"))
            for item in featured_points:
                FeaturedPoint.objects.create(
                    itinerary=itinerary,
                    suggested_date=item.get("suggestedDate"),
                    price=item.get("price"),
                    additional_information=item.get("additionalInformation"),
                )

            # Collect days from request
            days = []
            i = 0
            while f"days[{i}][title]" in request.data:
                day = {
                    "id": request.data.get(f"days[{i}][id]"),  # optional, if editing existing
                    "title": request.data.get(f"days[{i}][title]"),
                    "description": request.data.get(f"days[{i}][description]"),
                    "image": request.FILES.get(f"days[{i}][image]"),
                    "image_title": request.data.get(f"days[{i}][image_title]"),
                    "order" : i
                }
                days.append(day)
                i += 1

            existing_days_qs = Day.objects.filter(itinerary=itinerary)
            existing_ids = set(existing_days_qs.values_list('id', flat=True))

           # Get IDs from the request (exclude None, '', 'undefined')
            request_ids = set(
                int(item['id'])
                for item in days
                if item.get('id') not in [None, "", "undefined"]
            )
            # Delete days that are not in the request
            ids_to_delete = existing_ids - request_ids
            Day.objects.filter(id__in=ids_to_delete).delete()

            # Update or create days
            for day_data in days:
                day_id = day_data.pop("id", None)

                # Treat 'undefined' or empty string as no id (new object)
                if day_id in [None, "", "undefined"]:
                    # Create new Day
                    Day.objects.create(itinerary=itinerary, **day_data)
                else:
                    # Update existing Day
                    try:
                        day = Day.objects.get(id=day_id, itinerary=itinerary)
                        day.title = day_data["title"]
                        day.description = day_data["description"]
                        day.order = day_data["order"]

                        if day_data.get("image"):
                            day.image = day_data["image"]
                        day.image_title = day_data["image_title"]
                        day.save()
                    except Day.DoesNotExist:
                        # fallback: create if ID not found
                        Day.objects.create(itinerary=itinerary, **day_data)

            hotels = []
            i = 0
            while f"hotels[{i}][title]" in request.data:
                hotel = {
                    "id": request.data.get(f"hotels[{i}][id]"),  # optional, if editing existing
                    "title": request.data.get(f"hotels[{i}][title]"),
                    "description": request.data.get(f"hotels[{i}][description]"),
                    "image": request.FILES.get(f"hotels[{i}][image]"),
                    "coordinates": request.data.get(f"hotels[{i}][coordinates]"),
                    "location": request.data.get(f"hotels[{i}][location]"),
                    "map_link": request.data.get(f"hotels[{i}][mapLink]"),
                    "rating": request.data.get(f"hotels[{i}][rating]"),
                    "order" : i
                }
                hotels.append(hotel)
                i += 1
            

            existing_hotel_qs = Hotel.objects.filter(itinerary=itinerary)
            existing_ids = set(existing_hotel_qs.values_list('id', flat=True))

           # Get IDs from the request (exclude None, '', 'undefined')
            request_ids = set(
                int(item['id'])
                for item in hotels
                if item.get('id') not in [None, "", "undefined"]
            )

            # Delete hotels that are not in the request
            ids_to_delete = existing_ids - request_ids
            Hotel.objects.filter(id__in=ids_to_delete).delete()
            
                # Update or create hotels
            for hotel_data in hotels:
                    hotel_id = hotel_data.pop("id", None)

                    # Treat 'undefined' or empty string as new object
                    if hotel_id in [None, "", "undefined"]:
                        Hotel.objects.create(itinerary=itinerary, **hotel_data)
                    else:
                        try:
                            hotel = Hotel.objects.get(id=hotel_id, itinerary=itinerary)
                            hotel.title = hotel_data["title"]
                            hotel.description = hotel_data["description"]
                            if hotel_data.get("image"):
                                hotel.image = hotel_data["image"]
                            hotel.coordinates = hotel_data["coordinates"]
                            hotel.location = hotel_data["location"]
                            hotel.map_link = hotel_data["map_link"]
                            hotel.rating = hotel_data["rating"]
                            day.order = day_data["order"]
                            hotel.save()
                        except Hotel.DoesNotExist:
                            Hotel.objects.create(itinerary=itinerary, **hotel_data)
                

            gallery_items = []
            i = 0
            while f"gallery[{i}][title]" in request.data:
                item = {
                    "id": request.data.get(f"gallery[{i}][id]"),
                    "title": request.data.get(f"gallery[{i}][title]"),
                    "image": request.FILES.get(f"gallery[{i}][image]"),
                }
                gallery_items.append(item)
                i += 1
            # print(gallery_items)

            # Get all existing gallery IDs for this itinerary
            existing_gallery_qs = Gallery.objects.filter(itinerary=itinerary)
            existing_ids = set(existing_gallery_qs.values_list('id', flat=True))

            # Get IDs from the request (exclude None/empty)
           # Get IDs from the request (exclude None, '', 'undefined')
            request_ids = set(
                int(item['id'])
                for item in gallery_items
                if item.get('id') not in [None, "", "undefined"]
            )


            # Delete galleries that are not in the request
            ids_to_delete = existing_ids - request_ids
            Gallery.objects.filter(id__in=ids_to_delete).delete()

            # Create or update gallery items
            for item_data in gallery_items:
                # If you have an id field, you can handle updates similarly
                item_id = item_data.pop("id", None)
                
                if item_id in [None, "", "undefined"]:
                    Gallery.objects.create(itinerary=itinerary, **item_data)
                else:
                    try:
                        gallery_item = Gallery.objects.get(id=item_id, itinerary=itinerary)
                        gallery_item.title = item_data["title"]
                        if item_data.get("image"):
                            gallery_item.image = item_data["image"]
                        gallery_item.save()
                    except Gallery.DoesNotExist:
                        Gallery.objects.create(itinerary=itinerary, **item_data)

            return Response({"message": "Itinerary updated successfully!"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            transaction.set_rollback(True)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(['GET'])
def itinerary_list(request):

    categories = request.query_params.get('categories')
    destinations = request.query_params.get('destinations')
    countries = request.query_params.get('countries')
    collections = request.query_params.get('collections')

        
    itineraries = Itinerary.objects.filter(is_published=True).order_by('-created_at')

    # Filter for categories
    if categories:
        categories_list = categories.split(',')
        itineraries = itineraries.filter(category__in=categories_list)

    # Filter for destinations
    if destinations:
        destinations_list = destinations.split(',')
        itineraries = itineraries.filter(destination__in=destinations_list)

    # Filter for countries
    if countries:
        countries_list = countries.split(',')
        itineraries = itineraries.filter(country__in=countries_list)

    # Filter for collections
    if collections:
        collections_list = collections.split(',')
        itineraries = itineraries.filter(collection__in=collections_list)

     
    paginator = GeneralPagination()
    result_page = paginator.paginate_queryset(itineraries, request)

    serializer = ItineraryUserListingSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def itinerary_detail(request, pk):

        try:
            itinerary = get_object_or_404(Itinerary, pk=pk)
            serializer = UserItineraryDetailsSerializer(itinerary)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))



class CollectionsAdminAPIView(APIView):
    def get(self,request):
        collections = Collections.objects.all()
        serializer = CollectionsListSerializer(collections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @transaction.atomic
    def patch(self, request, pk):

        collection = get_object_or_404(Collections,pk=pk)

        data = request.data

        if not collection:
            return Response('We could not find the requested collection', status=status.HTTP_404_NOT_FOUND)
        
        collection.title = data.get("title", collection.title)
        collection.description = data.get("description", collection.description)

        if "banner_image" in request.FILES:
        #    include the collection.banner_image to trash
           collection.banner_image =  request.FILES["banner_image"]

        if "icon" in request.FILES:
            #    include the collection.banner_image to trash
           collection.icon =  request.FILES["icon"]

        collection.save()

        return Response({'message' :' Successfully updated the collection'}, status=status.HTTP_200_OK)



class DestinationsAdminAPIView(APIView):
    def get(self,request):
        destinations = Destinations.objects.all()
        serializer = DestinationsListSerializer(destinations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @transaction.atomic
    def patch(self, request, pk):

        destination = get_object_or_404(Destinations,pk=pk)

        data = request.data

        if not destination:
            return Response('We could not find the requested destination', status=status.HTTP_404_NOT_FOUND)
        
        destination.title = data.get("title", destination.title)
        destination.description = data.get("description", destination.description)

        if "banner_image" in request.FILES:
        #    include the collection.banner_image to trash
           destination.banner_image =  request.FILES["banner_image"]

        if "icon" in request.FILES:
            #    include the collection.banner_image to trash
           destination.icon =  request.FILES["icon"]

        destination.save()

        return Response({'message' :' Successfully updated the destination'}, status=status.HTTP_200_OK)





class CountriesAdminAPIView(APIView):

    def get(self,request):
        countries = Countries.objects.all()
        serializer = CountriesListSerializer(countries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def post(self,request):
        data = request.data

        title = data.get("title", '')
        destination = data.get("destination", '')
        destination_instance = get_object_or_404(Destinations,title=destination)

        Countries.objects.create(
            title=title,
            destination=destination_instance
        )

        return Response({'message' :' Successfully Created Country'}, status=status.HTTP_200_OK)
    
    def patch(self,request,pk):
        country = get_object_or_404(Countries,pk=pk)
        
        data = request.data

        title = data.get("title", '')
        destination = data.get("destination", '')
        destination_instance = get_object_or_404(Destinations,title=destination)

        country.title = title
        country.destination = destination_instance
        country.save()

        return Response({'message' :' Successfully Updated Country'}, status=status.HTTP_200_OK)
    
    def delete(self,request,pk):

        country = get_object_or_404(Countries,pk=pk)
        country.delete()
        return Response({'message' :'Country deleted from records.'}, status=status.HTTP_200_OK)




@api_view(['GET'])
def destination_list(request):
    destinations = Destinations.objects.values_list("title", flat=True)
    return Response(list(destinations), status=status.HTTP_200_OK)
    


