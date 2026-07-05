"""
Custom pagination for the NSE API.
"""
from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    """
    Page-number pagination that lets clients override the page size via
    ``?page_size=`` (capped), so a dashboard can pull every index in one
    request while list consumers keep a sane default.
    """
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 500
