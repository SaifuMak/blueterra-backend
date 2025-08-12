
from rest_framework.pagination import PageNumberPagination

class GeneralPagination(PageNumberPagination):
    page_size = 5

class JournalPagination(PageNumberPagination):
    page_size = 6

