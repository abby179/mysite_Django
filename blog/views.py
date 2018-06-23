from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Blog, BlogType


# Create your views here.
def blog_list(request):
    blog_all = Blog.objects.all()
    paginator = Paginator(blog_all, 10)
    page_num = request.GET.get('page', 1)
    # todo: add 404 page
    blog_page = paginator.get_page(page_num)

    context = {}
    context['blogs'] = blog_page.object_list
    context['blog_page'] = blog_page
    context['blog_types'] = BlogType.objects.all()
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, blog_pk):
    context = {}
    context['blog'] = get_object_or_404(Blog, id=blog_pk)
    return render(request, 'blog/blog_detail.html', context)


def blogs_with_type(request, blog_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)

    blog_all = Blog.objects.filter(blog_type=blog_type)
    paginator = Paginator(blog_all, 10)
    page_num = request.GET.get('page', 1)
    # todo: add 404 page
    blog_page = paginator.get_page(page_num)

    context['blogs'] = blog_page.object_list
    context['blog_page'] = blog_page
    context['blog_type'] = blog_type
    context['blog_types'] = BlogType.objects.all()
    return render(request, 'blog/blog_list.html', context)
