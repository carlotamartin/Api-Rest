from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, filters
from .models import Film, FilmGenre
from .serializers import FilmSerializer, FilmGenreSerializer
from django_filters.rest_framework import DjangoFilterBackend   # new
from rest_framework.pagination import PageNumberPagination  # new
from rest_framework.response import Response  # new




class ExtendedPagination(PageNumberPagination):
    page_size = 8

    def get_paginated_response(self, data):

        return Response({
            'count': self.page.paginator.count,
            'num_pages': self.page.paginator.num_pages,
            'page_number': self.page.number,
            'page_size': self.page_size,
            'next_link': self.get_next_link(),
            'previous_link': self.get_previous_link(),
            'results': data
        })



class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FilmGenre.objects.all()
    serializer_class = FilmGenreSerializer
    lookup_field = 'slug' # identificaremos los géneros usando su slug


class FilmViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer

    # Sistema de filtros
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    search_fields = ['title', 'year', 'genres__name']
    ordering_fields = ['title', 'year'] # new

    filterset_fields = {
    'year': ['lte', 'gte'],  # Año menor o igual, mayor o igual que
    'genres': ['exact']      # Género exacto
    }
    # Sistema de paginación
    pagination_class = ExtendedPagination
    pagination_class.page_size = 8  # películas por página


