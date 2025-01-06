from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """
    Custom pagination class that allows clients to control page size.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
