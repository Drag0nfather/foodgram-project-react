from rest_framework.viewsets import ReadOnlyModelViewSet

from recipe.models import Tag
from recipe.serializers import TagSerializer


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
