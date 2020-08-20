from django.conf.urls import url

from userapp import views

urlpatterns = [
    url(r'^register/$', views.RegisterView.as_view()),
    url(r'^checkUname/$',views.CheckUnameView.as_view()),
    #url(r'^login/$', )

]