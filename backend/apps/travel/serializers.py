from rest_framework.serializers import ModelSerializer
from .models import Destination,TravelPlan,TouristPlace

class DestinationSerializer(ModelSerializer):#becuase its reperesent of the django model we use modelserializer
    class Meta:
        model=Destination
        fields=["id","name","description","is_popular"]

class TravelPlanSerializer(ModelSerializer):
    class Meta:
        model=TravelPlan
        fields=["id","origin","destination","budget"]