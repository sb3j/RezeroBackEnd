from django.urls import path
from .views import  CreateOrderView, AcceptOrderView, RejectOrderView, OrderRequestListView, AcceptedOrderListView, CompanyNamesView, UserOrderListView, UserOrderDetailView 

urlpatterns = [
    path('order/', CreateOrderView.as_view(), name='create-order'),
    path('requests/', OrderRequestListView.as_view(), name='order-requests'),
    path('order-accept/<int:pk>/', AcceptOrderView.as_view(), name='order-accept'),
    path('order-reject/<int:pk>/', RejectOrderView.as_view(), name='order-reject'),
    path('accepted-orders/', AcceptedOrderListView.as_view(), name='accepted-orders'),
    path('company-names/', CompanyNamesView.as_view(), name='company-names'),
    path('user/orders/', UserOrderListView.as_view(), name='user-order-list'),
    path('user/orders/<int:pk>/', UserOrderDetailView.as_view(), name='user-order-detail'),
]
