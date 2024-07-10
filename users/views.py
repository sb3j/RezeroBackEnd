from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import IndividualUserCreationSerializer, BusinessUserCreationSerializer, IndividualUserLoginSerializer, BusinessUserLoginSerializer

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UserProfileSerializer


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



# class IndividualLoginView(generics.GenericAPIView):
#     serializer_class = IndividualUserLoginSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         try:
#             serializer.is_valid(raise_exception=True)
#         except Exception as e:
#             print("Validation Error:", str(e))
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#         user = serializer.validated_data['user']
#         tokens = serializer.get_tokens_for_user(user)
#         return Response(tokens, status=status.HTTP_200_OK)

# class BusinessLoginView(generics.GenericAPIView):
#     serializer_class = BusinessUserLoginSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         try:
#             serializer.is_valid(raise_exception=True)
#         except Exception as e:
#             print("Validation Error:", str(e))
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#         user = serializer.validated_data['user']
#         tokens = serializer.get_tokens_for_user(user)
#         return Response(tokens, status=status.HTTP_200_OK)


