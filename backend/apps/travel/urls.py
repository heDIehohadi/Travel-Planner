from django.urls import URLPattern,path
from .views import DestinationListView,DestinationRetrieveView
urlpatterns=[
    path("destinations/",DestinationListView.as_view()),
    path("destinations/<int:pk>/",DestinationRetrieveView.as_view())
]