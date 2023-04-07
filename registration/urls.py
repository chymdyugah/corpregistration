from django.urls import re_path as url
from . import views

app_name = 'registration'

urlpatterns = [
    url(r'^registration/$', views.RegisterView.as_view(), name='registration'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^corpmember/$', views.ListCorpMemberView.as_view(), name='list_corpmember'),
    url(r'^corpmember/(?P<pk>[0-9]+)/$', views.UpdateCorpMemberView.as_view(), name='edit_corpmember'),
    url(r'^corpmember/(?P<pk>[0-9]+)/delete/$', views.DeleteCorpMemberView.as_view(), name='delete_corpmember'),
    url(r'^corpmember/register/$', views.CreateCorpMembersView.as_view(), name='create_corpmember'),
    url(r'^$', views.RedirectHomeView.as_view(), name='home'),
]
