from django.http import Http404
from django.shortcuts import get_object_or_404
from geopy import Nominatim
from geopy.exc import GeocoderTimedOut
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from posts.models import Post, Comment, Like
from posts.serializers import PostSerializer, CommentSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        try:
            location = self.request.data.get('location', None)
            if location:
                geolocator = Nominatim(user_agent="myGeocoder")
                location_obj = geolocator.geocode(location)

                if location_obj:
                    latitude = location_obj.latitude
                    longitude = location_obj.longitude
                    serializer.save(author=self.request.user, latitude=latitude, longitude=longitude)
                else:
                    raise ValidationError("Не удалось найти координаты для указанного местоположения.")
            else:
                serializer.save(author=self.request.user)
        except GeocoderTimedOut:
            raise ValidationError("Время запроса к геокодеру истекло.")

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.author == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied("У вас нет прав изменять этот пост.")

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response({'detail': 'Пост успешно удален'}, status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        comment = serializer.instance
        if comment.author != self.request.user:
            raise PermissionDenied("У вас нет прав для редактирования этого комментария")
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response({'detail': 'Комментарий успешно удален'}, status=status.HTTP_204_NO_CONTENT)


class LikeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_pk'])
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
            return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
        return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)


class CoordinateView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        latitude = request.query_params.get('latitude', None)
        longitude = request.query_params.get('longitude', None)

        if latitude and longitude:
            try:
                geolocator = Nominatim(user_agent="myGeocoder")
                location = geolocator.reverse((latitude, longitude))
                if location:
                    return Response({'location_name': location.address}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Местоположение не найдено.'}, status=status.HTTP_404_NOT_FOUND)
            except GeocoderTimedOut:
                return Response({'error': 'Время запроса к геокодеру истекло.'}, status=status.HTTP_408_REQUEST_TIMEOUT)
        else:
            return Response({'error': 'Пожалуйста, укажите широту и долготу.'}, status=status.HTTP_400_BAD_REQUEST)
