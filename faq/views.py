from rest_framework import generics, filters
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.exceptions import ParseError
from django.db.models import Q
from .models import FAQ
from .serializers import FAQSerializer

class FAQListCreateAPIView(generics.ListCreateAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['category']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self):
        queryset = FAQ.objects.all()
        search_query = self.request.query_params.get('search', None)
        search_type = self.request.query_params.get('search_type', None)

        if search_query and search_type:
            if search_type == 'question':
                queryset = queryset.filter(question__icontains=search_query)
            elif search_type == 'answer':
                queryset = queryset.filter(answer__icontains=search_query)
            elif search_type == 'both':
                queryset = queryset.filter(Q(question__icontains=search_query) | Q(answer__icontains=search_query))
            else:
                raise ParseError(detail="Invalid search_type parameter. Valid values are 'question', 'answer', or 'both'.")
        return queryset

class FAQRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]
