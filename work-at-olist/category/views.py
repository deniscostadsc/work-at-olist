from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework.response import Response

from .models import Category, Channel
from .serializers import CategorySerializer, ChannelSerializer


class ChannelListView(views.APIView):
    def get(self, request, format=None):
        serializer = ChannelSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return Channel.objects.all()


class ChannelDetailView(views.APIView):
    def get(self, request, *args, **kwargs):
        get_object_or_404(self.get_queryset(), uid=kwargs['uid'])
        serializer = ChannelSerializer(Channel.objects.get(uid=kwargs['uid']))
        return Response(serializer.data)

    def get_queryset(self):
        return Channel.objects.all()


class CategoryListView(views.APIView):
    def get(self, request, format=None):
        serializer = CategorySerializer(
            self.get_queryset(), many=True, context={'request': request})
        return Response(serializer.data)

    def get_queryset(self):
        return Category.objects.all()


class CategoryDetailView(views.APIView):
    def get(self, request, *args, **kwargs):
        get_object_or_404(self.get_queryset(), uid=kwargs['uid'])
        serializer = CategorySerializer(
            Category.objects.get(uid=kwargs['uid']))
        return Response(serializer.data)

    def get_queryset(self):
        return Category.objects.all()
