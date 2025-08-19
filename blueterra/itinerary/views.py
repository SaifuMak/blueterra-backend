from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import *
import json
from  .serializers import ItinerarySerializer, ItineraryListSerializer
from  journals.paginations import GeneralPagination
from django.shortcuts import get_object_or_404



class ItineraryCreateAPIView(APIView):

    @transaction.atomic
    def post(self, request):
        try:
            is_published_str = request.data.getlist("is_published")

            if is_published_str:
                is_published_str = is_published_str[0]  # take first value

            is_published = str(is_published_str).lower() in ["true", "1", "yes"]

            print(is_published_str)  # should now be 'true' or 'false'
            print(is_published)      # should now be True/False


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
        
        itineraries = Itinerary.objects.all()

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
        