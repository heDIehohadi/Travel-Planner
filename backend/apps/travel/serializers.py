from rest_framework import serializers

from .models import Destination, TravelPlan


class DestinationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Destination
        fields = [
            "id",
            "name",
            "description",
            "type",
            "is_popular",
        ]


class TravelPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = TravelPlan
        fields = [
            "id",
            "origin",
            "destination",
            "travel_date_from",
            "travel_date_to",
            "budget_min",
            "budget_max",
            "currency",
        ]

    def validate(self, attrs):
        def current(field):
            # On PATCH, fields missing from the request keep their saved values.
            if field in attrs:
                return attrs[field]
            if self.instance is not None:
                return getattr(self.instance, field)
            return None

        destination = current("destination")
        travel_date_from = current("travel_date_from")
        travel_date_to = current("travel_date_to")

        budget_min = current("budget_min")
        budget_max = current("budget_max")

        if (
            travel_date_from
            and travel_date_to
            and travel_date_from > travel_date_to
        ):
            raise serializers.ValidationError(
                {
                    "travel_date_to": (
                        "travel_date_to must be greater than "
                        "or equal to travel_date_from."
                    )
                }
            )

        if (
            budget_min is not None
            and budget_max is not None
            and budget_min > budget_max
        ):
            raise serializers.ValidationError(
                {
                    "budget_max": (
                        "budget_max must be greater than "
                        "or equal to budget_min."
                    )
                }
            )

        if (
            destination is None
            and travel_date_from is None
            and travel_date_to is None
            and budget_min is None
            and budget_max is None
        ):
            raise serializers.ValidationError(
                "Provide at least one of: destination, budget, or travel dates."
            )

        return attrs