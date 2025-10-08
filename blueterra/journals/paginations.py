
from rest_framework.pagination import PageNumberPagination

class GeneralPagination(PageNumberPagination):
    page_size = 5

class ItineraryUsersPagination(PageNumberPagination):
    page_size = 6


class JournalPagination(PageNumberPagination):
    page_size = 6


class ItineraryListPagination(PageNumberPagination):
    page_size = 10