from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('individual', 'Individual'),
        ('business', 'Business'),
    )
    password1 = forms.CharField(
        label="비밀번호",
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="비밀번호 확인",
        strip=False,
        widget=forms.PasswordInput,
        help_text="위의 비밀번호와 동일하게 입력해 주세요.",
    )
    agree_terms = forms.BooleanField(label="이용약관 동의 (필수)", required=True)
    agree_privacy = forms.BooleanField(label="개인정보처리방침 동의 (필수)", required=True)
    receive_sms = forms.BooleanField(label="문자 수신 여부 (선택)", required=False)
    receive_email = forms.BooleanField(label="이메일 수신 여부 (선택)", required=False)
    nickname = forms.CharField(max_length=150, label="닉네임")
    phone = forms.CharField(max_length=15, label="전화번호 (선택)", required=False)
    address = forms.CharField(max_length=255, label="주소")
    detail_address = forms.CharField(max_length=255, label="상세주소")
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, label="회원 유형")

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'nickname', 'password1', 'password2', 'phone', 'address', 'detail_address', 'agree_terms', 'agree_privacy', 'receive_sms', 'receive_email', 'user_type')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "비밀번호가 일치하지 않습니다.")

        if not cleaned_data.get("agree_terms"):
            self.add_error('agree_terms', "이용약관에 동의해야 합니다.")

        if not cleaned_data.get("agree_privacy"):
            self.add_error('agree_privacy', "개인정보처리방침에 동의해야 합니다.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = self.cleaned_data['user_type']
        if commit:
            user.save()
        return user