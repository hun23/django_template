# CRUD
## 시작하기
1. settings.py 수정
  ```python
  TEMPLATES = [
    {
      ...,
      'DIRS': [BASE_DIR / 'templates']
    }
  ]
  STATIC_URL = '/static/'
  STATICFILES_DIRS = [
    BASE_DIR / 'static',
  ]
  MEDIA_URL = '/media/'
  MEDIA_ROOT = BASE_DIR / 'media'
  ```
2. mypjt와 같은 경로에 static, media, templates 폴더 생성
3. mypjt/urls.py 수정
```python
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('my_app/', include('my_app.urls')),
    path('accounts/', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
4. my_app/urls.py 수정
```python
from django.urls import path
from . import views

app_name = "my_app"
urlpatterns = [
    path("index/", views.index, name="index"),
    path('<int:pk>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/update/', views.update, name='update'),
]

```
## MODEL & Forms
1. models.py 수정
```python
from django.db import models

class Page(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    thumbnail = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```
2. forms.py 생성
```python
from django.db import models
from django import forms
from .models import Page

# Create your models here.
class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = "__all__"
```
3. migrate
```bash
python manage.py makemigrations
python manage.py migrate
```
----
## READ(index, detail)
1. import
```python
from django.shortcuts import render, redirect
from .models import 
```
2. index
```python
def index(request):
    page_list = Page.objects.all()
    context = {'page_list': page_list}
    return render(request, 'my_app/index.html', context)

```
3. detail
```python
def detail(request, pk):
    page = page.objects.get(pk=pk)
    context = {'page': page}
    return render(request, 'my_app/detail.html', context)
```
----
## CREATE & DELETE
1. import
```python
from .forms import PageForm
```
2. create
```python
def create(request):
    if request.method == 'POST':
        form = PageForm(request.POST, request.FILES)
        if form.is_valid():
            page = form.save()
            return redirect('my_app:detail', page.pk)
    else:
        form = PageForm()

    context = {'form': form}
    return render(request, 'my_app/create.html', context)
```
3. delete
```python
def delete(request, pk):
    page = page.objects.get(pk=pk)
    page.delete()
    return redirect('my_app:index')
```
----
## UPDATE
1. update
  - media 등 파일을 주고받기 위해서는 PageForm의 두번째 인자로 request.FILES를 넘거야 한다
```python
def update(request, pk):
    page = page.objects.get(pk=pk)

    if request.method == 'POST':
        form = PageForm(request.POST, request.FILES, instance=page)
        if form.is_valid():
            form.save()
            return redirect('my_app:detail', pk=page.pk)
    else:
        form = PageForm(instance=page)

    context = {'form': form, 'page': page}
    return render(request, 'my_app/update.html', context)
```
----
## HTMLs
1. index
```html
{% extends 'base.html' %} 

{% block content %}
  <h1>INDEX</h1>
  <a href="{% url 'my_app:create' %}">작성하기</a>
  <hr />

  {% for page in page_list %}
    <p>
      [{{page.id}}] <a href="{% url 'my_app:detail' page.pk %}" id="page-title">{{page.title}}</a>
    </p>
    <hr />
  {% endfor %} 

{% endblock content %}
```
2. detail
```html
{% extends 'base.html' %} 

{% block content %}
  <h1>DETAIL</h1>
  <hr />

  {% if page.image %}
    <img src="{{page.image.url}}" />
  {% endif %}

  <div id="page-content">
    <p>글 제목 : {{page.title}}</p>
    <p>글 내용 : {{page.content}}</p>
    <p>생성시각 : {{page.created_at}}</p>
    <p>수정시각 : {{page.updated_at}}</p>

    <hr>
    <a href="{% url 'my_app:update' page.pk %}">수정하기</a>
    <form action="{% url 'my_app:delete' page.pk %}" id="delete-form">
      {% csrf_token %}
      <input type="submit" value="삭제하기" id="delete-btn" />
    </form><br>
    <hr>
    <a href="{% url 'my_app:index' %}">목록보기</a>
  </div>
{% endblock content %}
```
3. create
```html
{% extends 'base.html' %} 

{% block content %}
  <h1>글작성</h1>
  <hr />

  <form
    action="{% url 'my_app:create' %}"
    method="POST"
    enctype="multipart/form-data">
    {% csrf_token %} {{form.as_p}}
    <input type="submit" value="작성하기"/>
  </form>

  <br />
  <hr>
  <a href="{% url 'my_app:index' %}">목록보기</a>
{% endblock content %}
```
4. update
```html
{% extends 'base.html' %} 

{% block content %}
  <h1>글수정</h1>
  <hr />

  <form action="{% url 'my_app:update' page.pk %}" method="POST"  enctype='multipart/form-data'>
    {% csrf_token %} {{form.as_p}}
    <input type="submit" />
  </form>

  <hr />
  <a href="{% url 'my_app:detail' page.pk %}">돌아가기</a>
{% endblock content %}
```
