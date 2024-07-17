from django.urls import path
from .views import (
    BusinessUserProfileView, ChangePasswordView, IndividualRegisterView, 
    BusinessRegisterView, IndividualLoginView, BusinessLoginView, 
    UserDeleteView, UserProfileView, UsernameCheckView, 
    NicknameCheckView, CompanyNameCheckView
)

urlpatterns = [
    path('register/', IndividualRegisterView.as_view(), name='individual-register'),
    path('register/b/', BusinessRegisterView.as_view(), name='business-register'),
    path('login/', IndividualLoginView.as_view(), name='individual-login'),
    path('login/b/', BusinessLoginView.as_view(), name='business-login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/b', BusinessUserProfileView.as_view(), name='business-user-profile'),
    path('del/', UserDeleteView.as_view(), name='user-delete'),
    path('pw/', ChangePasswordView.as_view(), name='change-password'),
    path('username-check/', UsernameCheckView.as_view(), name='username-check'),
    path('nickname-check/', NicknameCheckView.as_view(), name='nickname-check'),
    path('companyname-check/', CompanyNameCheckView.as_view(), name='companyname-check'),
]