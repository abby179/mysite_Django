import datetime
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from read_count.utils import get_seven_days_read_data, get_hot_today, get_hot_yesterday
from blog.models import Blog


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
