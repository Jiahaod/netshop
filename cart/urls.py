from django.conf.urls import *

from cart import views

urlpatterns = [
    url(r'^$', views.AddCartView.as_view()),
    url(r'^queryAll/$', views.CartListView.as_view()),
]