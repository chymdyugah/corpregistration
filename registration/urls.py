from django.urls import re_path as url
from . import views

app_name = 'registration'

urlpatterns = [
    url(r'^registration/$', views.RegisterView.as_view(), name='registration'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
]
