# AUTH
## 시작하기
1. accounts/models.py 수정
```python
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  pass
```
2. mypjt/settings.py 에 등록
```python
AUTH_USER_MODEL = 'accounts.User'
```
3. admin에 등록(옵션)
```python
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)
```
4. migrate
```bash
python manage.py makemigrations
python manage.py migrate
```
----
## urls.py
```python
from django.urls import path
form . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
    path('password/', views.change_password, name='change_password'),
    
]
```
----
## views.py
### login & logout
1. import
```python
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
```
2. login
```python
def login(request):
  if request.user.is_authenticated:  # login 되어있는 상태이면
    return redirect('my_app:index')  # index 페이지로
  if request.method == 'POST':
    # POST로 받은 데이터로 form 채우기
    form = AuthenticationForm(request, request.POST)
    if form.is_valid():  # 유효성 검증
      auth_login(request, form.get_user())  # form의 데이터로 로그인
      return redirect('my_app:index')
  else:
    form = AuthenticationForm()  # 빈 form
  
  context = {
    'form':form
    }
  return render(request, 'accounts/login.html', context)
```
3. logout
```python
def logout(request):
  auth_logout(request)
  return redirect('my_app:index')
```
### signup & update
1. forms.py 만들기
```python
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
```
2. views.py 수정
  - import
```python
from .forms import CustomUserCreationForm, CustomUserChangeForm
```
  - signup
```python
def signup(request):
  if request.method == "POST":
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
      # form.save()는 해당 form으로 user를 DB에 저장후
      # 해당 user를 반환
      user = form.save()
      auth_login(request, user)  # 가입 후 바로 로그인 처리
      return redirect('my_app:index')
  else:
    form = CustomUserCreationForm()
  
  context = {
    'form': form,

  }
  return render(request, 'accounts/signup.html', context)
```
  - update
```python
def update(request):
  if request.method == "POST":
    # "update" 위해 user instance 추가
    form = CustomUserChangeForm(request.POST, instance=request.user)
    if form.is_valid():
      form.save()
      return redirect('my_app:index')
  else:
    # user instacne를 추가해 데이터가 있는 form을 넘김
    form = CustomUserChangeForm(instance=request.user)
  
  context = {
    'form': form
  }
  return render(request, 'accounts/update.html', context)
```
----
## delete & change_password
1. import
   - PasswordChangeForm은 django의 user_model을 상속받지 않으므로, 이번 프로젝트에서 만든 accounts.User과 무관
   - 따라서 UserCreationForm처럼 Custom 한 모델을 만들 필요 없음
```python
from django.contrib.auth import update_session_auth_hash
from djang.contrib.auth.forms import ..., PasswordChangeForm
from django.views.decorators.http import require_http_methods, require_POST, require_safe
```
2. delete
```python
@require_http_methods(['POST'])  # require_POST와 동일
def delete(request):
  user = request.user
  user.delete()
  # 탈퇴 후 바로 로그아웃
  auth_logout(request)
  # 탈퇴 == DB에서 user 삭제 == DB 변경, 따라서 redirect
  return redirect('accounts:index')
```
3. change_password
```python
def change_password(request):
  if request.method == 'POST':
    form = PasswordChangeForm(request.user, request.POST)
    if form.is_valid():
      form.save()
      update_session_auth_hash(request, form.user)
      return redirect('my_app:index')
  else:
    form = PasswordChangeForm(request.user)
  
  context = {
    'form': form
  }
  return render(request, 'accounts/change_password.html', context)
```
----
## HTMLs
- login.html
```html
{% extends 'base.html' %}

{% block content %}
  <h1>Login</h1>
  <form action="{% url 'accounts:login' %}" method="POST">
    {% csrf_token %}
    {{form.as_p}}
    <input type="submit" value="로그인">
  </form>
{% endblock content %}

```
- update.html
```html
{% extends 'base.html' %}
{% block content %}
  <h1>회원정보수정</h1>
  <form action="{% url 'accounts:update' %}" method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="수정하기">
  </form>
  <a href="{% url 'my_app:index' %}">목록보기</a>
{% endblock content %}
```
- signup.html
```html
{% extends 'base.html' %}
{% block content %}
  <h1>회원가입</h1>
  <form action="{% url 'accounts:signup' %}" method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="회원가입">
  </form>
  <a href="{% url 'my_app:index' %}">목록보기</a>
{% endblock content %}
```
- change_password.html
```html
{% extends 'base.html' %}
{% block content %}
  <h1>비밀번호변경</h1>
  <form action="{% url 'accounts:change_password' %}" method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="변경하기">
  </form>
  <a href="{% url 'my_app:index' %}">목록보기</a>
{% endblock content %}
```