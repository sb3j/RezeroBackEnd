from django.urls import path
from .views import CompanyOrderListView, CompanyListView,  OrderUserDetailView, OrderAcceptRejectView

urlpatterns = [
    path('orders/', CompanyOrderListView.as_view(), name='company-order-list'),
    path('orders/<int:pk>/', OrderUserDetailView.as_view(), name='company-order-detail'),
    path('companies/', CompanyListView.as_view(), name='company-list'),
    path('orders/<int:order_id>/fix/', OrderAcceptRejectView.as_view(), name='order-accept-reject'),
]

