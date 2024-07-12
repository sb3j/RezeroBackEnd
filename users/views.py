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
            "프로필 사진": request.build_absolute_uri(instance.profile_picture.url) if instance.profile_picture else None
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
            "변경 프로필이미지": request.build_absolute_uri(instance.profile_picture.url) if instance.profile_picture else None
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