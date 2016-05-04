from django.conf.urls import url
from trades.views import TradeListView, TradeDetailView

__author__ = 'josebermudez'


urlpatterns = [
    url(r'^$', TradeListView.as_view(), name="list"),
    url(r'^(?P<pk>[\w\-]+)/$', TradeDetailView.as_view(), name="detail"),
]
