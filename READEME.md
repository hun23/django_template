# DJANGO
## 시작하기
1. 가상환경 설정
```bash
python -m venv venv
(윈도우) source venv/Scripts/activate
(맥) source venv/bin/activate
pip install django
pip install pillow
```
2. 프로젝트, 앱 생성
```bash
django-admin startproject mypjt .
python manage.py startapp my_app
python manage.py startapp accounts
```
3. settings.py 수정 (앱 연결)
```python
INSTALLED_APPS = [
    'my_app',
    'accounts',
    ...]
```
4. .gitignore 만들기
  - gitignore.io에서 django 로 검색 후 복사 붙여넣기
5. SECRET_KEY 숨기기(옵션)
  - 배포할 목적인 경우 settings.py의 SECRET_KEY를 git에 올리지 않기 위해 local_settings.py에 놓고 settings.py에서 import 하여 사용
  - gitignore.io에서 django로 .gitignore를 만들면 local_settings.py가 포함되어 있기 때문
----
## INDEX 페이지 만들기
1. settings.py 에서 mypjt로 url 넘기기
```python
from django.urls import path, include

urlpatterns = [
    ...,
    path('my_app/', include("my_app.urls")),
    path('accounts/', include('accounts.urls')),
]
```
2. mypjt 내에 urls.py 만들기
  - url이 들어오면 views.py 파일의 지정된 함수(views.index)가 실행되도록 한다.
```python
from django.urls import path
from . import views

app_name = "my_app"
urlpatterns = [
    path("index/", views.index, name="index"),
    
]
```
3. my_app의 views.py 수정하기
  - index 함수가 실행되면 my_app/templates/my_app/index.html을 그린다
  - templates 내에 my_app 폴더를 다시 만드는 이유?
```python
def index(request):
    return render(request, "my_app/index.html")
```
4. index.html 만들기
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>INDEX</title>
</head>
<body>
  <h1>INDEX</h1>
  <p>INDEX PAGE 입니다!</p>
</body>
</html>
```
----
## 실행하기
1. 서버 실행하기
```bash
python manage.py runserver
```
2. local 서버 들어가기
  - 브라우저 주소창에 ``` http://127.0.0.1:8000/ ``` 입력
3. index 페이지 들어가기
  - 위의 주소 뒤에 ```my_app/index``` 입력