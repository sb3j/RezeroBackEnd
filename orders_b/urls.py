from django.urls import path
from .views import AcceptedOrderListView, AcceptOrderView
from .views import OrderRequestListView, OrderDetailView

urlpatterns = [
    # 모든 주문 요청 목록 조회
    path('allOrder/', OrderRequestListView.as_view(), name='order-request-list'),
    
    # 특정 주문 요청의 상세 조회 (customer_order_number필요)
    path('detailOrder/<str:customer_order_number>/', OrderDetailView.as_view(), name='order-detail'),
    
    # 주문 수락 (customer_order_number필요)
    path('acceptOrder/<str:customer_order_number>/', AcceptOrderView.as_view(), name='accept-order'),
    
    # 수락된 주문 목록 조회
    path('aaOrders/', AcceptedOrderListView.as_view(), name='accepted-order-list'),
]


