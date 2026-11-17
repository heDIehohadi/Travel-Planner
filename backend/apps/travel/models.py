from django.db import models
from apps.accounts.models import User


class Destination(models.Model):

    class DestinationType(models.TextChoices):
        CITY = "CITY", "City"
        PROVINCE = "PROVINCE", "Province"

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(
        max_length=20,
        choices=DestinationType.choices,
    )
    is_popular = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class TouristPlace(models.Model):

    class PlaceType(models.TextChoices):
        HISTORICAL = "HISTORICAL", "Historical"
        NATURAL = "NATURAL", "Natural"
        MUSEUM = "MUSEUM", "Museum"
        BEACH = "BEACH", "Beach"
        RELIGIOUS = "RELIGIOUS", "Religious"
        ENTERTAINMENT = "ENTERTAINMENT", "Entertainment"

    name = models.CharField(max_length=255)
    destination = models.ForeignKey(
        Destination,
        on_delete=models.PROTECT,
        related_name="tourist_places",
    )
    type = models.CharField(
        max_length=20,
        choices=PlaceType.choices,
    )
    description = models.TextField()

    def __str__(self):
        return self.name


class TravelPlan(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        GENERATING = "GENERATING", "Generating"
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="travel_plans",
    )

    origin = models.ForeignKey(
        Destination,
        on_delete=models.PROTECT,
        related_name="origin_travel_plans",
        null=True,
        blank=True,
    )

    destination = models.ForeignKey(
        Destination,
        on_delete=models.PROTECT,
        related_name="destination_travel_plans",
    )

    travel_date_from = models.DateField(
        null=True,
        blank=True,
    )

    travel_date_to = models.DateField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    budget_min = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
    )

    budget_max = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
    )

    currency = models.CharField(
        max_length=3,
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    generated_plan = models.JSONField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.origin} → {self.destination}"