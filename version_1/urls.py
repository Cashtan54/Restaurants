from django.urls import path, include
from rest_framework import routers

from .views import RestaurantApiView, VoteAPIView

router = routers.DefaultRouter()
router.register('restaurant', RestaurantApiView, basename='restaraunt')
router.register('vote', VoteAPIView, basename='vote')

urlpatterns = [
    path('', include(router.urls)),
]
