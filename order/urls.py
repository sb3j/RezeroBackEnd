from django.urls import path
from .views import  CreateOrderView, AcceptOrderView, RejectOrderView, OrderRequestListView, AcceptedOrderListView

urlpatterns = [
    path('order/', CreateOrderView.as_view(), name='create-order'),
    path('requests/', OrderRequestListView.as_view(), name='order-requests'),
    path('order-accept/<int:pk>/', AcceptOrderView.as_view(), name='order-accept'),
    path('order-reject/<int:pk>/', RejectOrderView.as_view(), name='order-reject'),
    path('accepted-orders/', AcceptedOrderListView.as_view(), name='accepted-orders'),
]
