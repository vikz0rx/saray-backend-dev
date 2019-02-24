from rest_framework import serializers
from main.models import News

class NewsPreviewSerializer(serializers.ModelSerializer):
   class Meta:
       model = News
       fields = [
           'id',
           'title',
           'image',
           'created_at',
           'url',
       ]


class NewsDetailSerializer(serializers.ModelSerializer):
   class Meta:
       model = News
       fields = [
           'title',
           'image',
           'created_at',
           'url',
       ]