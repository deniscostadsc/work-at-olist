from rest_framework import serializers

from .models import Category, Channel


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    ancestors = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('name', 'uid', 'ancestors', 'children')

    def get_ancestors(self, obj):
        return [category.name
                for category in obj.get_ancestors()]

    def get_children(self, obj):
        return [category.name
                for category in obj.get_children()]


class ChannelSerializer(serializers.HyperlinkedModelSerializer):
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = ('name', 'uid', 'categories')

    def get_categories(self, obj):
        return [category.name
                for category in Category.objects.filter(channel=obj)]
