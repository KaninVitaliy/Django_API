from django_filters import rest_framework as filters

from posts.models import Post, Comment


class PostFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    # TODO: задайте требуемые фильтры

    class Meta:
        model = Post
        exclude = ['image']
        fields = "__all__"

