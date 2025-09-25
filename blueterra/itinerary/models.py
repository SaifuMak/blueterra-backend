from django.db import models
from blueterra.storages_backends import R2PublicStorage
from .mixins import R2PublicURLMixin
from blueterra.const import R2_PUBLIC_URL
from blueterra.utils import mark_file_for_deletion


class Collections(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    popular_journeys = models.CharField(max_length=2000,null=True, blank=True)
    banner_image = models.FileField(
        upload_to='collections/banners',
        storage=R2PublicStorage(),
        blank=True, null=True
    )
    icon = models.FileField(
        upload_to='collections/icons',
        storage=R2PublicStorage(),
        blank=True, null=True
    )

    banner_image_public_url  = models.URLField(null=True, blank=True)
    icon_public_url  = models.URLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
         
        base_url = R2_PUBLIC_URL

        updated_fields = []

        if self.banner_image:
                filename = self.banner_image.name
                new_url = f"{base_url}{filename}"
                if self.banner_image_public_url != new_url:
                    self.banner_image_public_url = new_url
                    updated_fields.append("banner_image_public_url")

        if self.icon:
                filename = self.icon.name
                new_url = f"{base_url}{filename}"
                if self.icon_public_url != new_url:
                    self.icon_public_url = new_url
                    updated_fields.append("icon_public_url")

        if updated_fields:
                super().save(update_fields=updated_fields)

    def __str__(self):
         return self.title
    


class Destinations(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    popular_journeys = models.CharField(max_length=2000,null=True, blank=True)
    banner_image = models.FileField(
        upload_to='destinations/banners',
        storage=R2PublicStorage(),
        blank=True, null=True
    )
    icon = models.FileField(
        upload_to='destinations/icons',
        storage=R2PublicStorage(),
        blank=True, null=True
    )

    banner_image_public_url  = models.URLField(null=True, blank=True)
    icon_public_url  = models.URLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
         
        base_url = R2_PUBLIC_URL

        updated_fields = []

        if self.banner_image:
                filename = self.banner_image.name
                new_url = f"{base_url}{filename}"
                if self.banner_image_public_url != new_url:
                    self.banner_image_public_url = new_url
                    updated_fields.append("banner_image_public_url")

        if self.icon:
                filename = self.icon.name
                new_url = f"{base_url}{filename}"
                if self.icon_public_url != new_url:
                    self.icon_public_url = new_url
                    updated_fields.append("icon_public_url")

        if updated_fields:
                super().save(update_fields=updated_fields)

    def __str__(self):
         return self.title


class Countries(models.Model):
    destination = models.ForeignKey(Destinations,on_delete=models.CASCADE, related_name="countries" )
    title = models.CharField(max_length=100)

    def __str__(self):
         return self.title

class Categories(models.Model):
    collection = models.ForeignKey(Collections,on_delete=models.CASCADE, related_name="categories" )
    title = models.CharField(max_length=100)

    def __str__(self):
         return self.title
    
# Create your models here.
class Itinerary(R2PublicURLMixin, models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    slug = models.TextField(unique=True,blank=True, null=True)
    location_title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=20, null=True, blank=True)
    general_rating = models.FloatField(default=5)
    is_published = models.BooleanField(default=False)
    destination = models.ForeignKey(Destinations, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey(Countries, on_delete=models.SET_NULL, null=True, blank=True)
    collection = models.ForeignKey(Collections, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    banner_image = models.FileField(
        upload_to='itinerary/banner',
        storage=R2PublicStorage(),
        blank=True, null=True
    )
    banner_image_public_url = models.URLField(blank=True, null=True)

    file_field_name = "banner_image"
    url_field_name = "banner_image_public_url"
    path_prefix="itinerary/banner"

    # def delete(self, *args, **kwargs):
    #     if self.banner_image:
    #         self.banner_image.delete(save=False)  # removes from R2
    #     super().delete(*args, **kwargs)  # removes model instance from DB

    def delete(self, *args, **kwargs):
        # mark itinerary banner
        if self.banner_image:
            mark_file_for_deletion(self.banner_image)

        # mark related Days images
        for day in self.days.all():
            if day.image:
                mark_file_for_deletion(day.image)

        # mark related Hotels images
        for hotel in self.hotels.all():
            if hotel.image:
                mark_file_for_deletion(hotel.image)

        # mark related Gallery images
        for gallery in self.gallery.all():
            if gallery.image:
                mark_file_for_deletion(gallery.image)

        # now delete the DB record and cascade relations
        super().delete(*args, **kwargs)


class Day(R2PublicURLMixin, models.Model):
    itinerary = models.ForeignKey(Itinerary, related_name="days", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    coordinates = models.CharField(max_length=255, blank=True, null=True)
    # image = models.ImageField(upload_to="days/", blank=True, null=True)
    image_title = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(default=0) 
    image = models.FileField(
        upload_to='itinerary/places',
        storage=R2PublicStorage(),
        blank=True, null=True
    )
    image_public_url = models.URLField(blank=True, null=True)

    file_field_name = "image"
    url_field_name = "image_public_url"
    path_prefix="itinerary/places"

    class Meta:
        ordering = ["order"]  # always return in saved order


class Hotel(R2PublicURLMixin, models.Model):
    itinerary = models.ForeignKey(Itinerary, related_name="hotels", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    coordinates = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    map_link = models.URLField(blank=True, null=True)
    rating = models.FloatField(default=0)
    order = models.PositiveIntegerField(default=0) 
    image = models.FileField(
        upload_to='itinerary/hotels',
        storage=R2PublicStorage(),
        blank=True, null=True
    )
    image_public_url = models.URLField(blank=True, null=True)

    file_field_name = "image"
    url_field_name = "image_public_url"
    path_prefix="itinerary/hotels"

    class Meta:
        ordering = ["order"]  # always return in saved order

class DestinationHighlight(models.Model):
    itinerary = models.ForeignKey(Itinerary, related_name="destination_highlights", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)


class SignatureHighlight(models.Model):
    itinerary = models.ForeignKey(Itinerary, related_name="signature_highlights", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)


class PackageInclusion(models.Model):
    itinerary = models.ForeignKey(Itinerary, related_name="package_inclusions", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)


class PackageExclusion(models.Model):
    itinerary = models.ForeignKey(Itinerary, related_name="package_exclusions", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)


class MapRouting(models.Model):
    itinerary = models.ForeignKey(Itinerary, related_name="map_routing", on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    coordinates = models.CharField(max_length=255)
    transfer = models.CharField(max_length=255, blank=True, null=True)


class Gallery(R2PublicURLMixin, models.Model):
    itinerary = models.ForeignKey(Itinerary, related_name="gallery", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    is_checked = models.BooleanField(default=False) 
    image = models.FileField(
        upload_to='itinerary/gallery',
        storage=R2PublicStorage(),
        blank=True, null=True
    )
    image_public_url = models.URLField(blank=True, null=True)

    file_field_name = "image"
    url_field_name = "image_public_url"
    path_prefix="itinerary/gallery"


class FeaturedPoint(models.Model):
    itinerary = models.ForeignKey(Itinerary, related_name="featured_points", on_delete=models.CASCADE)
    suggested_date = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    additional_information = models.CharField(max_length=255, blank=True, null=True)


class CruiseDeals(R2PublicURLMixin, models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.FileField(
        upload_to='cruise/deals',
        storage=R2PublicStorage(),
        blank=True, null=True
    )
    image_public_url = models.URLField(blank=True, null=True)
    is_published = models.BooleanField(default=True)

    file_field_name = "image"
    url_field_name = "image_public_url"
    path_prefix="cruise/deals"

    