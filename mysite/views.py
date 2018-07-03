import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.utils import timezone
from django.urls import reverse

from read_count.utils import get_seven_days_read_data, get_hot_today, get_hot_yesterday
from blog.models import Blog
from .forms import LoginForm, RegForm


def get_hot_blog_7_days():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=date)\
        .values('id', 'title').annotate(read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')
    return blogs[:7]


def index(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)

    # get caches for hot blogs in 7 days
    hot_7_days = cache.get('hot_7_days')
    if not hot_7_days:
        hot_7_days = get_hot_blog_7_days()
        cache.set('hot_7_days', hot_7_days, 3600)

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['hot_today'] = get_hot_today(blog_content_type)
    context['hot_yesterday'] = get_hot_yesterday(blog_content_type)
    context['hot_7_days'] = hot_7_days
    return render(request, 'index.html', context)


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('index')))
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)


def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            user.save()

            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('index')))

    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)
