from django.conf.urls import url


from order import views


urlpatterns=[
    url(r'^$',views.ToOrderView.as_view()),
    url(r'^order.html$',views.OrderListView.as_view()),
    url(r'^topay/$', views.ToPayViews.as_view()),
    url(r'^checkPay/$', views.CheckPayView.as_view()),

]