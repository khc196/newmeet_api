# party/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from .views import *

api_urlpattern = [
    path('parties/', PartyListView.as_view()),
    path('parties/<int:id>/', PartyDetailView.as_view()),
    path('parties/<int:id>/like/', PartyLikeView.as_view()),
    path('parties/<int:id>/comment/create/', PartyCommentCreateView.as_view()),
    path('places/<int:id>/', PlaceDetailView.as_view()),
]