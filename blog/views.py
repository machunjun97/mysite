from django.db.models import Count
from django.shortcuts import get_object_or_404, render

from comment.models import Comment
from reading_count.utils import *
from .models import Blog, BlogType


def blog_list(request):  # 博客列表
    page_range, page_of_blogs = pagination_exe(request)  # 分页范围，分页处理结果
    blog_dates_dict = get_date_classification()  # 按日期分类排序的文章

    context = {'page_of_blogs': page_of_blogs,
               "page_range": page_range,
               "blog_types": BlogType.objects.annotate(blog_count=Count('blog')),
               "blog_dates": blog_dates_dict
               }

    return render(request, "index.html", context)


def blog_detail(request, blog_pk):  # 博客详情

    blog = get_object_or_404(Blog, pk=blog_pk)  # pk:primary key
    read_cookie_key = reading_count_once_read(request, blog)
    content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=content_type, object_id=blog_pk)

    context = {'blog_detail': blog,
               'previous_blog': Blog.objects.filter(create_time__gt=blog.create_time).last(),
               'next_blog': Blog.objects.filter(create_time__lt=blog.create_time).first(),
               'comments': comments
               }

    response = render(request, "post.html", context)  # 响应
    response.set_cookie(read_cookie_key, 'true', max_age=60)  # 阅读cookie标记0

    return response


def blogs_with_type(request, blog_type_pk):  # 废弃
    context = {}
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    context["blogs"] = Blog.objects.filter(blog_type=blog_type)  # 符合条件的类别
    context["blogs_type"] = blog_type
    return render(request, "blogs_with_type.html", context)


def blogs_with_date(request, year, month):
    context = {"date": [year, month],
               "blogs": Blog.objects.filter(create_time__year=year, create_time__month=month)
               }
    return render(request, "blog_with_date.html", context)


def about(request):  # 关于页
    blog_content_type = ContentType.objects.get_for_model(Blog)  # 统计的数据类型
    read_num_statistics, dates = get_weekly_reading_date(blog_content_type)  # 阅读数据统计
    hot_blog_today = get_cache_data('hot_blog_today', blog_content_type)  # 从缓存中读取数据

    context = {'read_num_statistics': read_num_statistics,
               'dates': dates,
               'hot_data': hot_blog_today
               }

    return render(request, "about.html", context)


def contact(request):  # 联系页

    return render(request, "contact.html")

