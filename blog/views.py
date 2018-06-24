from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from .models import Blog, BlogType


# Create your views here.
def blog_list(request):
    blog_all = Blog.objects.all()
    paginator = Paginator(blog_all, settings.EACH_PAGE_BLOGS_NUMBER)
    page_num = request.GET.get('page', 1)
    # todo: add 404 page
    blog_page = paginator.get_page(page_num)
    current_page_num = blog_page.number
    page_range = list(range(max(current_page_num-2, 1), min(current_page_num+3, paginator.num_pages+1)))

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
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, blog_pk):
    context = {}
    blog = get_object_or_404(Blog, id=blog_pk)
    context['blog'] = blog
    context['previous_blog'] = Blog.objects.filter(create_time__gt=blog.create_time).last()
    context['next_blog'] = Blog.objects.filter(create_time__lt=blog.create_time).first()
    return render(request, 'blog/blog_detail.html', context)


def blogs_with_type(request, blog_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)

    blog_all = Blog.objects.filter(blog_type=blog_type)
    paginator = Paginator(blog_all, settings.EACH_PAGE_BLOGS_NUMBER)
    page_num = request.GET.get('page', 1)
    # todo: add 404 page
    blog_page = paginator.get_page(page_num)
    current_page_num = blog_page.number
    page_range = list(range(max(current_page_num-2, 1), min(current_page_num+3, paginator.num_pages+1)))

    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')

    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context['blogs'] = blog_page.object_list
    context['blog_page'] = blog_page
    context['blog_type'] = blog_type
    context['blog_types'] = BlogType.objects.all()
    context['page_range'] = page_range
    return render(request, 'blog/blog_list.html', context)
