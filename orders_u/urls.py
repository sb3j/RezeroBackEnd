from django.urls import path
from .views import CreateOrderUserView, UpdateOrderUserView,  DeleteOrderUserView

urlpatterns = [
    path('create/', CreateOrderUserView.as_view(), name='create-order-user'),
    path('update/<int:pk>/', UpdateOrderUserView.as_view(), name='update-order-user'),
    path('delete/<int:pk>/', DeleteOrderUserView.as_view(), name='delete-order-user'),
]