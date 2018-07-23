from django.conf.urls import url, include
from HashTag.views import *

urlpatterns = [

    # Example: /add/
    url(r'^add/$', HashTagCreateView.as_view(), name="add"),

    # Example: /99/update/
    # url(r'^(?P<pk2>\d+)/update/$', SKeywordUpdateView.as_view(), name="update"),

    # Example: /delete/
    # url(r'^(?P<pk2>\d+)/delete/$', SKeywordDeleteView.as_view(), name="delete"),
]
