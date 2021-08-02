from django_filters import BooleanFilter, FilterSet

from recipe.models import Recipe


class RecipeFilter(FilterSet):
    is_favorited = BooleanFilter(method='filter_is_favorited')

    class Meta:
        model = Recipe
        fields = ('tags', 'is_favorited', 'author')

    def filter_tags(self, queryset, slug, tags):
        tags = self.request.query_params.getlist('tags')
        return queryset.filter(tags__slug__in=tags).distinct()

    def filter_is_favorited(self, queryset):
        user = self.request.user
        if not user.is_authenticated:
            return queryset
        bool_dict = {'true': True, 'false': False}
        is_favorited = self.request.query_params.get('is_favorited', False)
        if bool_dict.get(is_favorited, False):
            return queryset.filter(
                is_favorited__user=self.request.user).distinct()
        return queryset
