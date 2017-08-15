from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views
from musicapp import views as local_views

router = routers.DefaultRouter()

router.register(r'bands', local_views.BandViewSet)
router.register(r'musicians', local_views.MusicianViewSet)
router.register(r'albums', local_views.AlbumViewSet)
router.register(r'band-members', local_views.BandMemberViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^token/', local_views.obtain_expiring_auth_token),
]