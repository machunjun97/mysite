# 工具
import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Sum
from .models import ReadNum, ReadingDetail
from blog.models import Blog


def reading_count_once_read(request, obj):  # 对阅读数进行统计
    ct = ContentType.objects.get_for_model(obj)
    key = f'{ct.model}_{obj.pk}_read'
    date = timezone.now().date()

    if not request.COOKIES.get(key):
        # 阅读数加一
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()

        # 当天阅读数加一
        read_detail, created = ReadingDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        read_detail.read_num += 1
        read_detail.save()
    return key


def get_weekly_reading_date(content_type):  # 统计一周网站文章的阅读数
    today = timezone.now().date()
    read_num_statistics = []
    dates = []
    for i in range(6, -1, -1):
        date = today - datetime.timedelta(days=i)
        reading_details = ReadingDetail.objects.filter(content_type=content_type, date=date)
        result = reading_details.aggregate(rn_sum=Sum('read_num'))  # 聚合
        read_num_statistics.append(result['rn_sum'] or 0)
        dates.append(date.strftime('%m/%d'))
    return read_num_statistics, dates


def get_today_hot_data(content_type):
    today = timezone.now().date()
    # 按阅读数降序
    reading_details = ReadingDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    if len(reading_details) > 5:
        reading_details = reading_details[0:6]
    return reading_details


def get_cache_data(cache_key, object_type):
    data = cache.get(cache_key)  # 从缓存中读取数据
    if data is None:
        hot_blog_today = get_today_hot_data(object_type)
        cache.set(cache_key, hot_blog_today, 600)
    return data


def pagination_exe(request):
    # 分页处理
    page_num = request.GET.get('page', 1)  # 获取url的页面参数
    blogs_all_list = Blog.objects.all()
    paginator = Paginator(blogs_all_list, 10)  # 10篇文章分页
    page_of_blogs = paginator.get_page(page_num)  # django帮你识别输入的页码是否合法
    current_page_num = page_of_blogs.number  # 获取当前页码
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) \
                + list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
    # 获取前后两个存在的页码

    # 加上首页和尾页码 没写
    # 加上省略标记 没写

    # 获取博客分类的数量
    # BlogType.objects.annotate(Count("blog"))  统计每一种博客的数量 SKL 并加到对象中

    return page_range, page_of_blogs


def get_date_classification():
    # 获取日期分类数量
    blog_dates = Blog.objects.dates('create_time', 'month', order="DESC")  # 获取Blog对象中所有的创建日期和月份
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(create_time__year=blog_date.year,
                                         create_time__month=blog_date.month).count()  # 获取对应年月的数量
        blog_dates_dict[blog_date] = blog_count  # 写入字典 键：日期 值：日期对应博客数量

    return blog_dates_dict
