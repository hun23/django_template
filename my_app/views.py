from django.shortcuts import render, redirect
from .models import Page
from .forms import PageForm

# Create your views here.
def index(request):
    page_list = Page.objects.all()
    context = {'page_list': page_list}
    return render(request, 'my_app/index.html', context)


def detail(request, pk):
    page = Page.objects.get(pk=pk)
    context = {'page': page}
    return render(request, 'my_app/detail.html', context)


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


def delete(request, pk):
    page = Page.objects.get(pk=pk)
    page.delete()
    return redirect('my_app:index')


def update(request, pk):
    page = Page.objects.get(pk=pk)

    if request.method == 'POST':
        form = PageForm(request.POST, request.FILES, instance=page)
        if form.is_valid():
            form.save()
            return redirect('my_app:detail', pk=page.pk)
    else:
        form = PageForm(instance=page)

    context = {'form': form, 'page': page}
    return render(request, 'my_app/update.html', context)
