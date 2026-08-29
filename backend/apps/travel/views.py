from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Destination
from .serializers import DestinationSerializer

class DestinationListView(ListAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

class DestinationRetrieveView(RetrieveAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer