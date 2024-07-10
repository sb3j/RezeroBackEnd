from django.urls import path
from .views import IndividualRegisterView, BusinessRegisterView,IndividualLoginView, BusinessLoginView, UserProfileView

urlpatterns = [
    path('register/individual/', IndividualRegisterView.as_view(), name='individual-register'),
    path('register/business/', BusinessRegisterView.as_view(), name='business-register'),
    path('login/individual/', IndividualLoginView.as_view(), name='individual-login'),
    path('login/business/', BusinessLoginView.as_view(), name='business-login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]
