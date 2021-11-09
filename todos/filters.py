from django_filters.rest_framework import FilterSet
from todos.models import Todo


class TodoFilter(FilterSet):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'is_complete')
