from django.db import IntegrityError
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Count
from .serializers import RegisterSerializer, RestaurantSerializer, VoteSerializer
from .models import User, Restaurant, Vote
from datetime import date


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class RestaurantApiView(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        restaurants = Restaurant.objects.all()
        return Response(RestaurantSerializer(restaurants, many=True).data)

    def retrive(self, request):
        restaurant = Restaurant.objects.get(name=request.data['name'])
        return Response({'restaraunt': RestaurantSerializer(restaurant).data})

    def create(self, request):
        data = {
            'name': request.data['name'],
        }
        restaurant = Restaurant.objects.create(name=data['name'], owner=request.user)
        return Response({'restaurant_created': RestaurantSerializer(restaurant).data})

    def patch(self, request, pk):
        data = {
            'menu_as_link': request.data['menu_as_link'],
        }
        restaurant = Restaurant.objects.get(pk=pk)
        if restaurant.owner == request.user:
            restaurant.menu_as_link = data['menu_as_link']
            restaurant.save()
            restaurant.refresh_from_db()
            return Response({'restaurant_updated': RestaurantSerializer(restaurant).data})
        else:
            return Response({'status': 'You are not the owner of restaurant'}, status=403)


class VoteAPIView(ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        restaurants = Vote.objects.filter(date=date.today()).values('restaurant__name').annotate(votes=Count('id')).order_by('votes')
        votes = dict()
        for rest in restaurants:
            votes[rest['restaurant__name']] = rest['votes']
        return Response(votes, status=200)

    def post(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        try:
            vote = Vote.objects.create(restaurant=restaurant, user=request.user)
            return Response({'voted': VoteSerializer(vote).data})
        except IntegrityError:
            return Response({'status': 'Already voted'}, status=200)

