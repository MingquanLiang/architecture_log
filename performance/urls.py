from django.conf.urls import include, url
#from django.contrib import admin

from .views import SearchIndexView
from .views import SearchResultView


urlpatterns = [
    url(r'^search_index/$', SearchIndexView.as_view(),
        name='search_index'),
    url(r'^search_result/$', SearchResultView.as_view(),
        name='search_result'),
]
