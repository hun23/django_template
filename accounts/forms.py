from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # accounts.User를 직접 지정하지 않고, Django 함수 사용
        # 혹시 project의 user_model을 수정할 때 작업의 용이성을 위해
        model = get_user_model()
        
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        models = get_user_model()
        fields = ('username', 'email', )  # 원하는 field만 입력