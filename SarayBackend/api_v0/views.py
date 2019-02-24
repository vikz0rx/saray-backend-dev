from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *

class NewsViewSet(viewsets.ReadOnlyModelViewSet):
   queryset = News.objects.all()

   def get_serializer_class(self):
       if self.action == 'list':
           return NewsPreviewSerializer
       return NewsDetailSerializer