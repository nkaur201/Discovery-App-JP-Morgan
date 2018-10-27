from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response

from discovery_api.models import Location, Warnings
from discovery_api.serializers import UserSerializer, LocationSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def create(self, request, *args, **kwargs):
        print(request.data["warnings"])
        warning_names = request.data["warnings"].lower().split(", ")
        actual_warnings = []

        for warningName in warning_names:
            existing_warnings = Warnings.objects.filter(name=warningName.strip())
            if len(existing_warnings) != 0:
                actual_warnings.append(existing_warnings.first().id)
            else:
                new_warning = Warnings.objects.create(name=warningName)
                new_warning.save()
                actual_warnings.append(new_warning.id)

        print(request.data)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()
