from django.conf.urls import url

from rest_framework.documentation import include_docs_urls

from .views import CategoryDetailView, ChannelListView, ChannelDetailView


urlpatterns = [
    url(r'^channel$', ChannelListView.as_view(), name='channels'),
    url(
        r'^channel/(?P<uid>[-\w]+)$',
        ChannelDetailView.as_view(), name='channel_detail'),
    url(r'^category/(?P<uid>[-\w]+)$',
        CategoryDetailView.as_view(), name='category_detail'),
    url(r'^', include_docs_urls(title='Olist API'))
]
