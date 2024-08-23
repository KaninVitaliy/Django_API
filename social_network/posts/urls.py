from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from posts import views
from django.conf.urls.static import static
from django.conf import settings

from posts.views import CoordinateView

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'posts/(?P<post_pk>\d+)/comments', views.CommentViewSet, basename='post-comments')
router.register(r'posts/(?P<post_pk>\d+)/likes', views.LikeViewSet, basename='post-likes')


urlpatterns = [
    path('api/', include(router.urls)),
    path('reverse-coordinates/', CoordinateView.as_view(), name='reverse-coordinates')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
