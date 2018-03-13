from django.conf.urls import url
from . import views
from django.conf.urls.static import static

app_name = 'Login'
urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    url(r'^login_user/$', views.UserLogin.as_view(), name='login_user'),

    url(r'^logout_user/$', views.logout_user, name='logout_user'),

    url(r'^(?P<pk>[0-9]+)/$',views.DetailView.as_view(), name='details'),

    url(r'^(?P<pk>[0-9]+)/create_song/$', views.create_song, name='create_song'),

    url(r'song_album/add/$',views.AlbumCreate.as_view(), name='album-add'),

    url(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.songs, name='songs'),

    url(r'^(?P<song_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),

    url(r'song_album/(?P<pk>[0-9]+)/$', views.AlbumUpdate.as_view(), name='album-update'),

    url(r'^(?P<pk>[0-9]+)/favorite_album/$', views.favorite_album, name='favorite_album'),

    url(r'^(?P<pk>[0-9]+)/delete_song/(?P<song_id>[0-9]+)/$', views.delete_song, name='delete_song'),

    url(r'song_album/(?P<pk>[0-9]+)/delete/$',views.AlbumDelete.as_view(), name='album-delete'),
]
