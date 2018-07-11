from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType

from .models import Blog, BlogType
from .forms import BlogForm
from read_count.utils import read_count_once


def get_common_blog_data(request, blog_all):
    paginator = Paginator(blog_all, settings.EACH_PAGE_BLOGS_NUMBER)
    page_num = request.GET.get('page', 1)
    blog_page = paginator.get_page(page_num)
    current_page_num = blog_page.number
    page_range = list(range(max(current_page_num - 2, 1), min(current_page_num + 3, paginator.num_pages + 1)))

    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')

    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {}
    context['blogs'] = blog_page.object_list
    context['blog_page'] = blog_page
    context['blog_types'] = BlogType.objects.all()
    context['page_range'] = page_range

    return context


def blog_list(request):
    blog_all = Blog.objects.all()
    context = get_common_blog_data(request, blog_all)
    return render(request, 'blog/blog_list.html', context)


def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blog_all = Blog.objects.filter(blog_type=blog_type)
    context = get_common_blog_data(request, blog_all)
    context['blog_type'] = blog_type
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, blog_pk):
    context = {}
    blog = get_object_or_404(Blog, id=blog_pk)
    read_cookie_key = read_count_once(request, blog)

    context['blog'] = blog
    context['previous_blog'] = Blog.objects.filter(create_time__gt=blog.create_time).last()
    context['next_blog'] = Blog.objects.filter(create_time__lt=blog.create_time).first()
    response = render(request, 'blog/blog_detail.html', context)
    response.set_cookie(read_cookie_key, 'true', max_age=120)
    return response


@login_required
def manage_blog(request):
    blog_all = Blog.objects.filter(author=request.user)
    return render(request, 'blog/manage_blog.html', {'blog_all': blog_all})


@login_required
def delete_blog(request, blog_pk):
    blog = get_object_or_404(Blog, id=blog_pk)
    if blog.author == request.user:
        blog.delete()
        messages.add_message(request, messages.SUCCESS, blog.title+' was deleted successfully.')
        return redirect('manage_blog')
    else:
        raise Http404('You are not allowed to delete this blog')


@login_required
def write_blog(request):
    if request.method == 'POST':
        blog_form = BlogForm(request.POST)
        if blog_form.is_valid():
            blog = Blog()
            blog.title = blog_form.cleaned_data['title']
            blog.blog_type = blog_form.cleaned_data['blog_type']
            blog.content = blog_form.cleaned_data['content']
            blog.author = request.user
            blog.save()
            messages.add_message(request, messages.SUCCESS, 'Article posted!')
            return redirect('manage_blog')
        else:
            messages.add_message(request, messages.WARNING, list(blog_form.errors.values())[0][0])

    context = {'blog_form': BlogForm()}
    return render(request, 'blog/write_blog.html', context)


@login_required
def edit_blog(request, blog_pk):
    blog = get_object_or_404(Blog, id=blog_pk)

    if request.method == 'POST':
        blog_form = BlogForm(request.POST)
        if blog_form.is_valid():
            blog.title = blog_form.cleaned_data['title']
            blog.blog_type = blog_form.cleaned_data['blog_type']
            blog.content = blog_form.cleaned_data['content']
            blog.save()
            messages.add_message(request, messages.SUCCESS, 'Article updated!')
            return redirect('blog_detail', blog.pk)
        else:
            messages.add_message(request, messages.WARNING, list(blog_form.errors.values())[0][0])

    blog_form = BlogForm(initial={'title': blog.title, 'content': blog.content, 'blog_type': blog.blog_type})
    context = {'blog_form': blog_form}
    return render(request, 'blog/edit_blog.html', context)
