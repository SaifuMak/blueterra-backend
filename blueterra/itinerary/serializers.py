from rest_framework import serializers
from .models import (
    Itinerary, Day, Hotel, DestinationHighlight, SignatureHighlight,
    PackageInclusion, PackageExclusion, MapRouting, Gallery, FeaturedPoint
)

class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        exclude = ("id", "itinerary")


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        exclude = ("id", "itinerary")


class DestinationHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = DestinationHighlight
        exclude = ("id", "itinerary")


class SignatureHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignatureHighlight
        exclude = ("id", "itinerary")


class PackageInclusionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageInclusion
        exclude = ("id", "itinerary")


class PackageExclusionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageExclusion
        exclude = ("id", "itinerary")


class MapRoutingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapRouting
        exclude = ("id", "itinerary")


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        exclude = ("id", "itinerary")


class FeaturedPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturedPoint
        exclude = ("id", "itinerary")


class ItinerarySerializer(serializers.ModelSerializer):
    days = DaySerializer(many=True, read_only=True)
    hotels = HotelSerializer(many=True, read_only=True)
    destination_highlights = DestinationHighlightSerializer(many=True, read_only=True)
    signature_highlights = SignatureHighlightSerializer(many=True, read_only=True)
    package_inclusions = PackageInclusionSerializer(many=True, read_only=True)
    package_exclusions = PackageExclusionSerializer(many=True, read_only=True)
    map_routing = MapRoutingSerializer(many=True, read_only=True)
    gallery = GallerySerializer(many=True, read_only=True)
    featured_points = FeaturedPointSerializer(many=True, read_only=True)

    class Meta:
        model = Itinerary
        fields = "__all__"


class ItineraryListSerializer(serializers.ModelSerializer):
    days = DaySerializer(many=True, read_only=True)

    class Meta:
        model = Itinerary
        fields = ['title','collection','days']
