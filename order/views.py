from rest_framework import generics, permissions, status
from rest_framework.response import Response
from order.serializers import OrderSerializer, OrderRequestSerializer, FixSerializer
from .pagination import StandardResultsSetPagination
from rest_framework import generics, filters
from .models import Order, Fix
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions, filters
from .models import Order
from .serializers import UserOrderSerializer, UserOrderDetailSerializer
from .pagination import StandardResultsSetPagination
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Order, Fix
from .serializers import FixSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from users.models import CustomUser
from drf_yasg.utils import swagger_auto_schema

# 주문 생성뷰
@swagger_auto_schema(
    operation_description="Create a new order",
    request_body=OrderSerializer,
    responses={201: "Order created successfully", 400: "Bad Request"}
)
class CreateOrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


# 주문 거절 뷰
@swagger_auto_schema(
    operation_description="Reject an order",
    responses={200: "Order rejected successfully", 403: "Permission denied", 404: "Order not found"}
)
class RejectOrderView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        if order.business_user != request.user:
            return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        order.status = '거절'
        order.save()
        return Response({"detail": "주문을 거절했습니다."}, status=status.HTTP_200_OK)


# 기업사용자 주문요청리스트뷰
@swagger_auto_schema(
    operation_description="Retrieve the list of order requests for a business user",
    responses={200: "Request list retrieved successfully"}
)
class OrderRequestListView(generics.ListAPIView):
    serializer_class = OrderRequestSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    search_fields = ['user__nickname', 'id']

    def get_queryset(self):
        user = self.request.user
        if user.user_type != 'business':
            return Order.objects.none()
        return Order.objects.filter(business_user=user, status__in=['pending', '대기'])


# 주문 수락뷰
@swagger_auto_schema(
    operation_description="Accept an order",
    responses={200: "Order accepted successfully", 400: "Bad Request", 404: "Order not found"}
)
class AcceptOrderView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        order_id = self.kwargs.get('pk')
        try:
            order = Order.objects.get(id=order_id, business_user=request.user)
            fix, created = Fix.objects.get_or_create(
                order=order,
                user_nickname=order.user.nickname,
                material=order.material,
                category=order.category,
                color=order.color,
                created_at=order.created_at,
                business_user=request.user
            )
            if created:
                fix.save()
                order.status = '수락'
                order.save()
                return Response({"detail": "Order accepted."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "This order is already accepted."}, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found or you do not have permission to accept this order."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 수락주문리스트뷰
@swagger_auto_schema(
    operation_description="Retrieve the list of accepted orders for a business user",
    responses={200: "Accepted orders list retrieved successfully"}
)
class AcceptedOrderListView(generics.ListAPIView):
    serializer_class = FixSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['created_at', 'fixed_at']
    ordering = ['-created_at']
    search_fields = ['id', 'user_nickname']

    def get_queryset(self):
        user = self.request.user
        if user.user_type != 'business':
            return Fix.objects.none()
        return Fix.objects.filter(business_user=user)


# 기업이름 조회뷰
@swagger_auto_schema(
    operation_description="Retrieve the list of company names",
    responses={200: "Company names list retrieved successfully"}
)
class CompanyNamesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        business_users = CustomUser.objects.filter(user_type='business')
        company_names = business_users.values_list('company_name', flat=True)
        return Response(list(company_names), status=status.HTTP_200_OK)


# 사용자의 주문내역뷰
@swagger_auto_schema(
    operation_description="Retrieve the list of orders for a user",
    responses={200: "User order list retrieved successfully"}
)
class UserOrderListView(generics.ListAPIView):
    serializer_class = UserOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


# 사용자 주문 상세뷰
@swagger_auto_schema(
    operation_description="Retrieve details of a specific order for a user",
    responses={200: "User order detail retrieved successfully"}
)
class UserOrderDetailView(generics.RetrieveAPIView):
    serializer_class = UserOrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)