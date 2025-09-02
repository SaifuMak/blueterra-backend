from django.db import models
from blueterra.storages_backends import R2PublicStorage
from .mixins import R2PublicURLMixin


# Create your models here.
class Itinerary(R2PublicURLMixin, models.Model):
    title = models.CharField(max_length=255)
    location_title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=20)
    # banner_image = models.ImageField(upload_to="banners/", blank=True, null=True)

    destination = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    collection = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    banner_image = models.FileField(
        upload_to='itinerary/',
        storage=R2PublicStorage(),
        blank=True, null=True
    )
    banner_image_public_url = models.URLField(blank=True, null=True)

    file_field_name = "banner_image"
    url_field_name = "banner_image_public_url"

    def delete(self, *args, **kwargs):
        if self.banner_image:
            self.banner_image.delete(save=False)  # removes from R2
        super().delete(*args, **kwargs)  # removes model instance from DB


class Day(R2PublicURLMixin, models.Model):
    itinerary = models.ForeignKey(Itinerary, related_name="days", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    # image = models.ImageField(upload_to="days/", blank=True, null=True)
    image_title = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(default=0) 
    image = models.FileField(
        upload_to='itinerary/',
        storage=R2PublicStorage(),
        blank=True, null=True
    )
    image_public_url = models.URLField(blank=True, null=True)

    file_field_name = "image"
    url_field_name = "image_public_url"

    class Meta:
        ordering = ["order"]  # always return in saved order



class Hotel(R2PublicURLMixin, models.Model):
    itinerary = models.ForeignKey(Itinerary, related_name="hotels", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    coordinates = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    map_link = models.URLField(blank=True, null=True)
    rating = models.FloatField(default=0)
    order = models.PositiveIntegerField(default=0) 
    image = models.FileField(
        upload_to='itinerary/',
        storage=R2PublicStorage(),
        blank=True, null=True
    )
    image_public_url = models.URLField(blank=True, null=True)

    file_field_name = "image"
    url_field_name = "image_public_url"

    class Meta:
        ordering = ["order"]  # always return in saved order

class DestinationHighlight(models.Model):
    itinerary = models.ForeignKey(Itinerary, related_name="destination_highlights", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)


class SignatureHighlight(models.Model):
    itinerary = models.ForeignKey(Itinerary, related_name="signature_highlights", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)


class PackageInclusion(models.Model):
    itinerary = models.ForeignKey(Itinerary, related_name="package_inclusions", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)


class PackageExclusion(models.Model):
    itinerary = models.ForeignKey(Itinerary, related_name="package_exclusions", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)


class MapRouting(models.Model):
    itinerary = models.ForeignKey(Itinerary, related_name="map_routing", on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    coordinates = models.CharField(max_length=255)
    transfer = models.CharField(max_length=255, blank=True, null=True)


class Gallery(R2PublicURLMixin, models.Model):
    itinerary = models.ForeignKey(Itinerary, related_name="gallery", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.FileField(
        upload_to='itinerary/',
        storage=R2PublicStorage(),
        blank=True, null=True
    )
    image_public_url = models.URLField(blank=True, null=True)

    file_field_name = "image"
    url_field_name = "image_public_url"


class FeaturedPoint(models.Model):
    itinerary = models.ForeignKey(Itinerary, related_name="featured_points", on_delete=models.CASCADE)
    suggested_date = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    additional_information = models.CharField(max_length=255, blank=True, null=True)


class Collections(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    banner_image = models.FileField(
        upload_to='collections/',
        storage=R2PublicStorage(),
        blank=True, null=True
    )
    icon = models.FileField(
        upload_to='collections/',
        storage=R2PublicStorage(),
        blank=True, null=True
    )

    banner_image_public_url  = models.URLField(null=True, blank=True)
    icon_public_url  = models.URLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
         
        base_url = "https://pub-c75e3733f0bd4a078b015afdd3afc354.r2.dev/"

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
    banner_image = models.FileField(
        upload_to='destinations/',
        storage=R2PublicStorage(),
        blank=True, null=True
    )
    icon = models.FileField(
        upload_to='destinations/',
        storage=R2PublicStorage(),
        blank=True, null=True
    )

    banner_image_public_url  = models.URLField(null=True, blank=True)
    icon_public_url  = models.URLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
         
        base_url = "https://pub-c75e3733f0bd4a078b015afdd3afc354.r2.dev/"

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
