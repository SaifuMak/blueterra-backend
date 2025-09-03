from rest_framework import serializers
from .models import (
    Itinerary, Day, Hotel, DestinationHighlight, SignatureHighlight,
    PackageInclusion, PackageExclusion, MapRouting, Gallery, FeaturedPoint, Collections, Destinations, Countries, Categories
)

class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        exclude =  ["itinerary"] 


class DayUserItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields =  ["id"] 

class UserDayDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        exclude = ["id", "itinerary", "image"]


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        exclude =  ["itinerary"] 

class UserHotelDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        exclude = ["id", "itinerary", "image"]


class DestinationHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = DestinationHighlight
        exclude =   ["itinerary"] 

class UserDestinationHighlightDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DestinationHighlight
        exclude = ["id", "itinerary"]


class SignatureHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignatureHighlight
        exclude =  ["itinerary"] 


class UserSignatureHighlightDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignatureHighlight
        exclude = ["id", "itinerary"]



class PackageInclusionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageInclusion
        exclude =  ["itinerary"] 

class UserPackageInclusionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageInclusion
        exclude = ["id", "itinerary"]

class PackageExclusionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageExclusion
        exclude =  ["itinerary"] 

class UserPackageExclusionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageExclusion
        exclude = ["id", "itinerary"]


class MapRoutingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapRouting
        exclude =  ["itinerary"] 

class UserMapRoutingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapRouting
        exclude = ["id", "itinerary"]



class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        exclude =  ["itinerary"] 


class UserGalleryDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        exclude = ["id", "itinerary", "image"]
        
class GalleryUserItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        exclude =  ["itinerary","image"] 



class FeaturedPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturedPoint
        exclude =  ["itinerary"] 


class UserFeaturedPointDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturedPoint
        exclude =  ["id","itinerary"] 


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





class UserItineraryDetailsSerializer(serializers.ModelSerializer):
    days = UserDayDetailsSerializer(many=True, read_only=True)
    hotels = UserHotelDetailsSerializer(many=True, read_only=True)
    destination_highlights = UserDestinationHighlightDetailsSerializer(many=True, read_only=True)
    signature_highlights = UserSignatureHighlightDetailsSerializer(many=True, read_only=True)
    package_inclusions = UserPackageInclusionDetailsSerializer(many=True, read_only=True)
    package_exclusions = UserPackageExclusionDetailsSerializer(many=True, read_only=True)
    map_routing = UserMapRoutingDetailsSerializer(many=True, read_only=True)
    gallery = UserGalleryDetailsSerializer(many=True, read_only=True)
    featured_points = UserFeaturedPointDetailsSerializer(many=True, read_only=True)


    class Meta:
        model = Itinerary
        exclude = [
            "is_published",
            "created_at",
            "updated_at",
            "banner_image",
        ]



class CollectionsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collections
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ["title"]


class CollectionsListUserSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True) 
    class Meta:
        model = Collections
        fields = ['title','description','banner_image_public_url','icon_public_url','categories']


class DestinationsListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collections
        fields = ['title','description','banner_image_public_url','icon_public_url']

class DestinationsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Destinations
        fields = '__all__'


class DestinationsFilterListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Destinations
        fields = ['title']

class CollectionsFilterListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collections
        fields = ['title']

# class CategoriesFilterListSerializer(serializers.ModelSerializer):
#     collection = CollectionsFilterListSerializer(read_only=True)
#     class Meta:
#         model = Categories
#         fields = '__all__'

# class CountriesFilterListSerializer(serializers.ModelSerializer):
#     destination = DestinationsFilterListSerializer(read_only=True)

#     class Meta:
#         model = Collections
#         fields = '__all__'

class CountriesListSerializer(serializers.ModelSerializer):
    destination = DestinationsFilterListSerializer(read_only=True)
    class Meta:
        model = Countries
        fields = '__all__'

class CategoriesListSerializer(serializers.ModelSerializer):
    collection = CollectionsFilterListSerializer(read_only=True)
    class Meta:
        model = Categories
        fields = '__all__'



class ItineraryDetailsSerializer(serializers.ModelSerializer):

    destination = DestinationsFilterListSerializer(read_only=True)
    collection = CollectionsFilterListSerializer(read_only=True)
    country = CountriesListSerializer(read_only=True)
    category = CategoriesListSerializer(read_only=True)

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
        fields = '__all__'


class ItineraryListSerializer(serializers.ModelSerializer):
    days = DaySerializer(many=True, read_only=True)
    collection = CollectionsFilterListSerializer(read_only=True)

    class Meta:
        model = Itinerary
        fields = ['id','title','collection','is_published','days']



class ItineraryUserListingSerializer(serializers.ModelSerializer):
    days = DayUserItinerarySerializer(many=True, read_only=True)
    gallery = GalleryUserItinerarySerializer(many=True, read_only=True)
    category = CategoriesListSerializer(read_only=True)

    class Meta:
        model = Itinerary
        fields = ['id','title','location_title','description','collection','category','is_published','days','gallery']
