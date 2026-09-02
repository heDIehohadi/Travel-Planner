from rest_framework.generics import ListCreateAPIView,ListAPIView,RetrieveUpdateDestroyAPIView,RetrieveAPIView
from .models import Destination,TravelPlan
from .serializers import DestinationSerializer,TravelPlanSerializer
from rest_framework.permissions import IsAuthenticated

class DestinationListView(ListAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

class DestinationRetrieveView(RetrieveAPIView):

    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

class TravelPlanListCreateView(ListCreateAPIView):

    serializer_class=TravelPlanSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):#for this request assigned which objects allowed to enter the queryset
        return TravelPlan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)# Assign the owner to the current authenticated user

class TravelPlanRetrieveView(RetrieveUpdateDestroyAPIView):

    serializer_class=TravelPlanSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return TravelPlan.objects.filter(user=self.request.user)