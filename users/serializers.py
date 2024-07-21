from rest_framework import serializers
from django.contrib.auth import authenticate, password_validation
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password

#개인회원 가입
class IndividualUserCreationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[password_validation.validate_password])
    verifyPW = serializers.CharField(write_only=True, required=True)
    agree_terms = serializers.BooleanField(write_only=True, required=True)
    agree_privacy = serializers.BooleanField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'nickname', 'password', 'verifyPW', 'phone', 'address', 'detail_address', 'agree_terms', 'agree_privacy', 'receive_sms', 'receive_email')

    def validate(self, attrs):
        if attrs['password'] != attrs['verifyPW']:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})

        if not attrs.get('agree_terms') or not attrs.get('agree_privacy'):
            raise serializers.ValidationError({"agree_terms": "이용약관 및 개인정보처리방침에 동의해야 합니다."})

        return attrs

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            nickname=validated_data['nickname'],
            phone=validated_data['phone'],
            address=validated_data['address'],
            detail_address=validated_data['detail_address'],
            receive_sms=validated_data.get('receive_sms', False),
            receive_email=validated_data.get('receive_email', False),
            user_type='individual'
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

#기업 회원가입
class BusinessUserCreationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[password_validation.validate_password])
    verifyPW = serializers.CharField(write_only=True, required=True)
    agree_terms = serializers.BooleanField(write_only=True, required=True)
    agree_privacy = serializers.BooleanField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'nickname', 'business_registration_number', 'company_name', 'password', 'verifyPW', 'phone', 'address', 'detail_address', 'agree_terms', 'agree_privacy', 'receive_sms', 'receive_email')

    def validate(self, attrs):
        if attrs['password'] != attrs['verifyPW']:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})

        if not attrs.get('agree_terms') or not attrs.get('agree_privacy'):
            raise serializers.ValidationError({"agree_terms": "이용약관 및 개인정보처리방침에 동의해야 합니다."})

        if CustomUser.objects.filter(company_name=attrs['company_name'], user_type='business').exists():
            raise serializers.ValidationError({"company_name": "이 회사 이름은 이미 사용 중입니다."})

        return attrs

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            nickname=validated_data['nickname'],
            business_registration_number=validated_data['business_registration_number'],
            company_name=validated_data['company_name'],
            phone=validated_data['phone'],
            address=validated_data['address'],
            detail_address=validated_data['detail_address'],
            receive_sms=validated_data.get('receive_sms', False),
            receive_email=validated_data.get('receive_email', False),
            user_type='business'
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

#개인회원 로그인
class IndividualUserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        print(f"Attempting to authenticate individual user: {username}")

        if username and password:
            user = authenticate(username=username, password=password)
            if user and user.user_type == 'individual':
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError("사용자가 비활성화되었습니다.")
            else:
                print(f"Authentication failed for individual user: {username}")
                raise serializers.ValidationError("사용자 인증에 실패했습니다.")
        else:
            raise serializers.ValidationError("사용자명과 비밀번호를 모두 입력해야 합니다.")

        return data

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

#개인회원 정보조회
class UserProfileSerializer(serializers.ModelSerializer):
    orders_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'nickname', 'phone', 'address', 'detail_address', 'profile_picture', 'user_type', 'orders_count']
        extra_kwargs = {
            'username': {'read_only': True},
            'user_type': {'read_only': True},
            'phone': {'required': False, 'allow_blank': True},
            'profile_picture': {'required': False, 'allow_null': True}
        }

#기업회원 정보조회
class BusinessUserProfileSerializer(serializers.ModelSerializer):
    order_requests_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'nickname', 'phone', 'company_name', 'address', 'detail_address', 'profile_picture', 'order_requests_count']
        extra_kwargs = {
            'username': {'read_only': False},
            'phone': {'required': False, 'allow_blank': True},
            'profile_picture': {'required': False, 'allow_null': True}
        }

#기업회원 로그인
class BusinessUserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        print(f"Attempting to authenticate business user: {username}")

        if username and password:
            user = authenticate(username=username, password=password)
            if user and user.user_type == 'business':
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError("사용자가 비활성화되었습니다.")
            else:
                print(f"Authentication failed for business user: {username}")
                raise serializers.ValidationError("사용자 인증에 실패했습니다.")
        else:
            raise serializers.ValidationError("사용자명과 비밀번호를 모두 입력해야 합니다.")

        return data

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

#사용자 탈퇴
class UserDeleteSerializer(serializers.Serializer):
    agree_terms = serializers.BooleanField(write_only=True)
    reason = serializers.CharField(write_only=True, required=False, allow_blank=True)

    def validate_agree_terms(self, value):
        if not value:
            raise serializers.ValidationError("탈퇴 동의는 필수입니다.")
        return value

#비밀번호 변경
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    verify_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("현재 비밀번호가 일치하지 않습니다.")
        return value

    def validate(self, data):
        if data['new_password'] != data['verify_password']:
            raise serializers.ValidationError("새로운 비밀번호가 일치하지 않습니다.")
        password_validation.validate_password(data['new_password'])
        return data
    
    
#사용자 아이디 중복체크
class UsernameCheckSerializer(serializers.Serializer):
    username = serializers.CharField()

#닉네임 중복체크
class NicknameCheckSerializer(serializers.Serializer):
    nickname = serializers.CharField()

#기업이름 중복체크
class CompanyNameCheckSerializer(serializers.Serializer):
    company_name = serializers.CharField()
    


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
#토큰 재발급
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        credentials = {
            'username': attrs.get('username'),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                if not user.is_active:
                    raise serializers.ValidationError('User account is disabled.')
            else:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "username" and "password".')

        data = super().validate(attrs)
        data['user'] = user
        return data



from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
#리프레쉬 토큰 재발급
class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = RefreshToken(attrs['refresh'])
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data
