from django.urls import path, include
from .views import RestaurantApiView


urlpatterns = [
    path('restaurant/', RestaurantApiView.as_view(), name='restaraunt'),

]
