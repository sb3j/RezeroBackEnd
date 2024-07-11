from rest_framework import generics
from .models import Order
from .serializers import OrderSerializer
from rest_framework.pagination import PageNumberPagination

class OrderPagination(PageNumberPagination):
    page_size = 10

class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderPagination