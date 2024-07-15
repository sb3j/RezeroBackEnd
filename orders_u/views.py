from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import OrderUser
from .serializers import OrderUserSerializer
from .permissions import IsIndividualUser
from orders_b.models import Company 

class CreateOrderUserView(generics.CreateAPIView):
    serializer_class = OrderUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # AI 모델이 이미지를 분석하여 category, material, color를 결정합니다.
        # 예: ai_model.predict(image) => {'category': 'sweater', 'material': 'cotton', 'color': 'green'}
        ai_result = {'category': 'sweater', 'material': 'cotton', 'color': 'green'}  # 예제 AI 결과
        category = ai_result['category']
        material = ai_result['material']
        color = ai_result['color']

        data = request.data
        data['category'] = category
        data['material'] = material
        data['color'] = color

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            response_data = {
                "order_id": serializer.data['id'],
                "nickname": request.user.nickname,
                "username": request.user.username,
                "created_at": serializer.data['created_at']
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import OrderUser
from .serializers import OrderUserSerializer
from .permissions import IsIndividualUser

class UpdateOrderUserView(generics.UpdateAPIView):
    queryset = OrderUser.objects.all()
    serializer_class = OrderUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsIndividualUser]

    def get_queryset(self):
        return OrderUser.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data

        if 'company_id' in data:
            try:
                company = Company.objects.get(id=data['company_id'])
                data['company'] = company.id
            except Company.DoesNotExist:
                return Response({"error": "Invalid company ID"}, status=status.HTTP_400_BAD_REQUEST)

        # 카테고리에 따라 수정 가능한 필드 설정
        if instance.category == 'shirt':
            valid_fields = ['sleeve_length', 'neckline', 'pocket', 'etc', 'company']
        elif instance.category == 'sweater':
            valid_fields = ['sleeve_length', 'neckline', 'button', 'zipper', 'etc', 'company']
        else:
            return Response({"error": "Invalid category"}, status=status.HTTP_400_BAD_REQUEST)

        for field in data.keys():
            if field not in valid_fields:
                return Response({"error": f"Field '{field}' cannot be updated for category '{instance.category}'"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteOrderUserView(generics.DestroyAPIView):
    queryset = OrderUser.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsIndividualUser]

    def get_queryset(self):
        return OrderUser.objects.filter(user=self.request.user)