from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, RestaurantSerializer
from .models import User, Restaurant


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class RestaurantApiView(APIView):
    queryset = Restaurant.objects.all()

    def get(self, request):
        restaurant = Restaurant.objects.get(name=request.data['name'])
        return Response({'restaraunt': RestaurantSerializer(restaurant).data})

    def post(self, request):
        data = {
            'name': request.data['name'],
        }
        restaurant = Restaurant.objects.create(name=data['name'], owner=request.user)
        return Response({'restaurant_created': RestaurantSerializer(restaurant).data})

    def patch(self, request):
        data = {
            'name': request.data['name'],
            'menu_as_link': request.data['menu_as_link'],
        }
        restaurant = Restaurant.objects.get(name=data['name'])
        if restaurant.owner == request.user:
            restaurant.menu_as_link = data['menu_as_link']
            restaurant.save()
            restaurant.refresh_from_db()
            return Response({'restaurant_updated': RestaurantSerializer(restaurant).data})
        else:
            return Response({'status': 'You are not the owner of restaurant'}, status=403)
