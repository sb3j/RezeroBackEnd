from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import CustomTokenRefreshSerializer, IndividualUserCreationSerializer, BusinessUserCreationSerializer, IndividualUserLoginSerializer, BusinessUserLoginSerializer, UserDeleteSerializer

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UserProfileSerializer
from .serializers import BusinessUserProfileSerializer 

from rest_framework.permissions import IsAuthenticated
from .serializers import ChangePasswordSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UsernameCheckSerializer, NicknameCheckSerializer, CompanyNameCheckSerializer
from rest_framework import views, status



class IndividualRegisterView(generics.GenericAPIView):
    serializer_class = IndividualUserCreationSerializer
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입이 완료되었습니다."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BusinessRegisterView(generics.GenericAPIView):
    serializer_class = BusinessUserCreationSerializer
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입이 완료되었습니다."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IndividualLoginView(generics.GenericAPIView):
    serializer_class = IndividualUserLoginSerializer
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            print("Validation Error:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']
        tokens = serializer.get_tokens_for_user(user)

        response = Response(status=status.HTTP_200_OK)
        response['Authorization'] = 'Bearer ' + tokens['access']
        response['Refresh-Token'] = tokens['refresh']
        return response

class BusinessLoginView(generics.GenericAPIView):
    serializer_class = BusinessUserLoginSerializer
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            print("Validation Error:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']
        tokens = serializer.get_tokens_for_user(user)

        response = Response(status=status.HTTP_200_OK)
        response['Authorization'] = 'Bearer ' + tokens['access']
        response['Refresh-Token'] = tokens['refresh']
        return response

from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import CustomUser
from .serializers import UserProfileSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        response_data = {
            "변경 아이디": serializer.validated_data.get('username', instance.username),
            "변경 닉네임": serializer.validated_data.get('nickname', instance.nickname),
            "변경 전화번호": serializer.validated_data.get('phone', instance.phone),
            "변경 주소": serializer.validated_data.get('address', instance.address),
            "변경 상세주소": serializer.validated_data.get('detail_address', instance.detail_address),
            "프로필 사진": request.build_absolute_uri(instance.profile_picture.url) if instance.profile_picture else None,
            "orders_count": instance.orders_count  # 추가된 부분
        }

        return Response(response_data, status=status.HTTP_200_OK)

class BusinessUserProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.filter(user_type='business')
    serializer_class = BusinessUserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        response_data = {
            "변경 아이디": serializer.validated_data.get('username', instance.username),
            "변경 닉네임": serializer.validated_data.get('nickname', instance.nickname),
            "변경 전화번호": serializer.validated_data.get('phone', instance.phone),
            "변경 주소": serializer.validated_data.get('address', instance.address),
            "변경 상세주소": serializer.validated_data.get('detail_address', instance.detail_address),
            "변경 프로필이미지": request.build_absolute_uri(instance.profile_picture.url) if instance.profile_picture else None,
            "order_requests_count": instance.order_requests_count  # 추가된 부분
        }

        return Response(response_data, status=status.HTTP_200_OK)

class UserDeleteView(generics.GenericAPIView):
    serializer_class = UserDeleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        reason = serializer.validated_data.get('reason', '')
        print(f"User {user.username} is being deleted for reason: {reason}")

        user.delete()

        return Response({"message": "사용자가 성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
    
    
    

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = self.get_object()
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "비밀번호가 성공적으로 변경되었습니다."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    


class UsernameCheckView(views.APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = UsernameCheckSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            if CustomUser.objects.filter(username=username).exists():
                return Response({"available": False, "message": "Username is already taken."}, status=status.HTTP_200_OK)
            return Response({"available": True, "message": "Username is available."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NicknameCheckView(views.APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = NicknameCheckSerializer(data=request.data)
        if serializer.is_valid():
            nickname = serializer.validated_data['nickname']
            if CustomUser.objects.filter(nickname=nickname).exists():
                return Response({"available": False, "message": "Nickname is already taken."}, status=status.HTTP_200_OK)
            return Response({"available": True, "message": "Nickname is available."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanyNameCheckView(views.APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = CompanyNameCheckSerializer(data=request.data)
        if serializer.is_valid():
            company_name = serializer.validated_data['company_name']
            if CustomUser.objects.filter(company_name=company_name, user_type='business').exists():
                return Response({"available": False, "message": "Company name is already taken."}, status=status.HTTP_200_OK)
            return Response({"available": True, "message": "Company name is available."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']
        refresh = serializer.validated_data['refresh']
        access = serializer.validated_data['access']

        response = Response(status=status.HTTP_200_OK)
        response['Authorization'] = 'Bearer ' + str(access)
        response['Refresh-Token'] = str(refresh)
        return response



from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.response import Response
from rest_framework import status

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        refresh = serializer.validated_data['refresh']
        access = serializer.validated_data['access']

        response = Response(status=status.HTTP_200_OK)
        response['Authorization'] = 'Bearer ' + str(access)
        response['Refresh-Token'] = str(refresh)
        return response
