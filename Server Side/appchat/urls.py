from django.conf.urls import url, include

import views


urlpatterns = [
    url(r'^testing/$', views.testing),
    url(r'^common/$', views.CommonUrl.as_view()),
    url(r'^url/?$', views.ChatBot.as_view()),
]
