import django_filters
from .models import ReceiveOrder

class ReceiveOrderFilter(django_filters.FilterSet):
    customer_nickname = django_filters.CharFilter(field_name='customer__username', lookup_expr='icontains')
    customer_order_number = django_filters.CharFilter(field_name='customer_order_number', lookup_expr='icontains')
    order_date = django_filters.OrderingFilter(
        fields=(
            ('order_date', 'order_date'),
        ),
        field_labels={
            'order_date': '주문일자',
        },
    )

    class Meta:
        model = ReceiveOrder
        fields = ['customer_nickname', 'customer_order_number']
