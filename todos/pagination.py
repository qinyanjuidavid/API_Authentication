from rest_framework import pagination


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 3
    page_query_param = 'page'
    page_size_query_params = 'per_page'
    max_page_size = 100000
