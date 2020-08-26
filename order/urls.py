from django.conf.urls import url

from cart import views
from order.views import *


urlpatterns=[
    url(r'^$',views.ToOrderView.as_view()),
    url(r'^order.html$',views.OrderListView.as_view()),

]