import datetime

from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .renderers import UserJSONRenderer
from .serializers import *

class RegistrationAPIView(APIView):
    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class LocationsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny, )
    queryset = Locations.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return LocationsPreviewSerializer
        return LocationsDetailSerializer

class PhotographsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny, )
    queryset = Photographs.objects.all()

    def get_serializer_class(self):
        return PhotographsDetailSerializer

class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny, )
    queryset = News.objects.filter(approved=True)

    def get_serializer_class(self):
        if self.action == 'list':
            return NewsPreviewSerializer
        return NewsDetailSerializer

class BookingTypesViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny, )
    queryset = BookingTypes.objects.all()

    def get_serializer_class(self):
        return BookingTypesDetailSerializer

class BookingOptionsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny, )
    queryset = BookingOptions.objects.all()

    def get_serializer_class(self):
        return BookingOptionsDetailSerializer

class BookingsRentTimeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Bookings.objects.filter(status=Bookings.IS_PAYED)
    serializer_class = BookingsRentTimeSerializer

    def get_queryset(self):
        if (len(self.request.GET) >= 3):
            data = self.request.GET
            year = int(data['year'])
            month = int(data['month'])
            day = int(data['day'])
            # location = int(data['location'])

        return Bookings.objects.filter(date=datetime.date(year, month, day), status=Bookings.IS_PAYED)

class BookingsViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, )
    queryset = Bookings.objects.filter(status=Bookings.IS_PAYED)

    def get_serializer_class(self):
        if self.action == 'list':
            return BookingsPreviewSerializer
        return BookingsDetailSerializer