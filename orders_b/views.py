from rest_framework import generics, permissions, filters, status
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from orders_b.models import Fix
from orders_u.models import OrderUser  
from orders_b.serializers import OrderUserListSerializer, FixSerializer
from orders_b.permissions import IsCompanyUser




class OrderUserPagination(PageNumberPagination):
    page_size = 10

class CompanyOrderListView(generics.ListAPIView):
    serializer_class = OrderUserListSerializer
    permission_classes = [permissions.IsAuthenticated, IsCompanyUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    pagination_class = OrderUserPagination

    def get_queryset(self):
        return OrderUser.objects.filter(company=self.request.user.company)

from rest_framework import generics
from .models import Company
from .serializers import CompanySerializer
class CompanyListView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]  
    
    

from rest_framework import generics, permissions
from orders_u.models import OrderUser
from .serializers import OrderUserDetailSerializer
from .permissions import IsCompanyUser

class OrderUserDetailView(generics.RetrieveAPIView):
    queryset = OrderUser.objects.all()
    serializer_class = OrderUserDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsCompanyUser]

    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')

        try:
            order = OrderUser.objects.get(id=order_id, company=request.user.company)
        except OrderUser.DoesNotExist:
            return Response({"error": "Order not found or not authorized."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)



class OrderAcceptRejectView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, IsCompanyUser]

    def post(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        action = request.data.get('action')

        try:
            order = OrderUser.objects.get(id=order_id, company=request.user.company)
        except OrderUser.DoesNotExist:
            return Response({"error": "Order not found or not authorized."}, status=status.HTTP_404_NOT_FOUND)

        if action == 'accept':
            fix = Fix.objects.create(
                user=order.user,
                company=order.company,
                category=order.category,
                sleeve_length=order.sleeve_length,
                neckline=order.neckline,
                pocket=order.pocket,
                etc=order.etc,
                material=order.material,  # 추가된 필드
                color=order.color  # 추가된 필드
            )
            order.delete()
            return Response({"message": "Order accepted and moved to Fix.", "fix": FixSerializer(fix).data}, status=status.HTTP_200_OK)
        elif action == 'reject':
            order.delete()
            return Response({"message": "Order rejected and deleted."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)