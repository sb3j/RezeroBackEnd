from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import ReceiveOrder
from .serializers import ReceiveOrderRequestListSerializer, ReceiveOrderSerializer, ReceiveOrderListSerializer
from .pagination import StandardResultsSetPagination
from .filters import ReceiveOrderFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


# 모든 주문 요청 목록 조회, 디폴트가 최신순
class OrderRequestListView(generics.ListAPIView):
    queryset = ReceiveOrder.objects.all()
    serializer_class = ReceiveOrderRequestListSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ReceiveOrderFilter
    ordering_fields = ['order_date']
    ordering = ['-order_date']  



 # 특정 주문 요청의 상세 조회 (customer_order_number필요)
class OrderDetailView(generics.RetrieveAPIView):
    queryset = ReceiveOrder.objects.all()
    serializer_class = ReceiveOrderSerializer
    permission_classes = [AllowAny]
    lookup_field = 'customer_order_number'


# 주문 수락 (customer_order_number필요)
class AcceptOrderView(generics.UpdateAPIView):
    queryset = ReceiveOrder.objects.all()
    serializer_class = ReceiveOrderSerializer
    permission_classes = [AllowAny]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'accepted'
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)



# 수락된 주문 목록 조회
class AcceptedOrderListView(generics.ListAPIView):
    queryset = ReceiveOrder.objects.filter(status='accepted')
    serializer_class = ReceiveOrderListSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination