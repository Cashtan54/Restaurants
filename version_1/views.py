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

    def create(self, request):
        data = {
            'name': request.data['name'],
        }
        try:
            restaurant = Restaurant.objects.create(name=data['name'], owner=request.user)
            return Response(RestaurantSerializer(restaurant).data)
        except IntegrityError:
            return Response({'status': 'Restaurant with this name already exist'}, status=200)

    def partial_update(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        if restaurant.owner == request.user:
            restaurant.menu_as_link = request.data['menu_as_link']
            restaurant.save()
            return Response(RestaurantSerializer(restaurant).data)
        else:
            return Response({'error': 'You are not the owner of this restourant'}, status=200)


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
