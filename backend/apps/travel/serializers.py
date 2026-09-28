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
        travel_date_from = attrs.get("travel_date_from")
        travel_date_to = attrs.get("travel_date_to")

        budget_min = attrs.get("budget_min")
        budget_max = attrs.get("budget_max")

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

        return attrs