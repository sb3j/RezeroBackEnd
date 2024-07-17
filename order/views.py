from rest_framework import generics, permissions, status
from rest_framework.response import Response
from order.serializers import OrderSerializer, OrderRequestSerializer, FixSerializer
from .pagination import StandardResultsSetPagination
from .models import Order, Fix
from rest_framework.permissions import IsAuthenticated

class CreateOrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

class RejectOrderView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        if order.business_user != request.user:
            return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        # Order 삭제
        order.delete()
        return Response({"detail": "주문을 거절했습니다."}, status=status.HTTP_200_OK)

class OrderRequestListView(generics.ListAPIView):
    serializer_class = OrderRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if user.user_type != 'business':
            return Order.objects.none()  # 비즈니스 사용자가 아닌 경우 빈 쿼리셋 반환
        return Order.objects.filter(business_user=user).order_by('-created_at')


class AcceptOrderView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        order_id = self.kwargs.get('pk')
        try:
            order = Order.objects.get(id=order_id, business_user=request.user)
            fix, created = Fix.objects.get_or_create(
                user_nickname=order.user.nickname,
                material=order.material,
                category=order.category,
                color=order.color,
                created_at=order.created_at,
                business_user=request.user
            )
            if not created:
                return Response({"detail": "This order is already accepted."}, status=status.HTTP_400_BAD_REQUEST)

            order.delete()  # 원래 Order에서 삭제
            return Response({"detail": "Order accepted."}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found or you do not have permission to accept this order."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class AcceptedOrderListView(generics.ListAPIView):
    serializer_class = FixSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if user.user_type != 'business':
            return Fix.objects.none()  # 비즈니스 사용자가 아닌 경우 빈 쿼리셋 반환
        return Fix.objects.filter(business_user=user).order_by('-fixed_at')
    
    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from users.models import CustomUser

class CompanyNamesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        business_users = CustomUser.objects.filter(user_type='business')
        company_names = business_users.values_list('company_name', flat=True)
        return Response(list(company_names), status=status.HTTP_200_OK)
