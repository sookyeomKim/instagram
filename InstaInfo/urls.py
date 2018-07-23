from django.conf.urls import url, include
from InstaInfo.views import *

urlpatterns = [
    url(r'^$', InstaInfoListView.as_view(), name='index'),

    # Example: /2
    url(r'^(?P<pk>\d+)/$', InstaInfoDetailView.as_view(), name='detail'),

    # Example: /add/
    url(r'^add/$', InstaInfoCreateView.as_view(), name="add"),

    # Example: /99/update/
    url(r'^(?P<pk2>\d+)/update/$', InstaInfoUpdateView.as_view(), name="update"),

    # Example: /delete/
    url(r'^(?P<pk2>\d+)/delete/$', InstaInfoDeleteView.as_view(), name="delete"),

    url(r'^(?P<pk>\d+)/hashtag/', include('HashTag.urls', namespace='hashtag'))
]
