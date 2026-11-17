from django.urls import path
from .views import TravelPlanRetrieveView,DestinationListView,DestinationRetrieveView,TravelPlanListCreateView
urlpatterns=[
    path("destinations/",DestinationListView.as_view()),
    path("destinations/<int:pk>/",DestinationRetrieveView.as_view()),
    path("plans/",TravelPlanListCreateView.as_view()),
    path("plans/<int:pk>/",TravelPlanRetrieveView.as_view())
]