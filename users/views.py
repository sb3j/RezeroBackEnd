from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import IndividualUserCreationSerializer, BusinessUserCreationSerializer, IndividualUserLoginSerializer, BusinessUserLoginSerializer, UserDeleteSerializer

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UserProfileSerializer
from .serializers import BusinessUserProfileSerializer 

from rest_framework.permissions import IsAuthenticated
from .serializers import ChangePasswordSerializer
from rest_framework import generics, status
from rest_framework.response import Response

class IndividualRegisterView(generics.GenericAPIView):
    serializer_class = IndividualUserCreationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입이 완료되었습니다."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BusinessRegisterView(generics.GenericAPIView):
    serializer_class = BusinessUserCreationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입이 완료되었습니다."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IndividualLoginView(generics.GenericAPIView):
    serializer_class = IndividualUserLoginSerializer

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


class BusinessUserProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.filter(user_type='business')
    serializer_class = BusinessUserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser,)

    def get_object(self):
        return self.request.user


class UserDeleteView(generics.GenericAPIView):
    serializer_class = UserDeleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        reason = serializer.validated_data.get('reason', '')
        # 여기서 필요하다면 탈퇴 이유를 로그로 남기거나 별도 처리할 수 있습니다.
        print(f"User {user.username} is being deleted for reason: {reason}")

        user.delete()

        return Response({"detail": "사용자가 성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
    
    
    

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
            return Response({"detail": "비밀번호가 성공적으로 변경되었습니다."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)