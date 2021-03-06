from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from .models import Blog, BlogType
from read_statistics.utils import read_statistics_once_read

# Create your views here.


def get_blog_list_common_data(request, blogs_all_list):
    # 进行分页
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER)
    # 获取页码参数（GET请求）
    page_num = request.GET.get('page', 1)
    page_of_blogs = paginator.get_page(page_num)
    # 获取当前页码
    current_page_num = page_of_blogs.number
    page_range = list(range(max(current_page_num - 2, 1),
                      min(paginator.num_pages + 1, current_page_num + 3)))
    # 加上省略页码标记
    if page_range[0] > 2:
        page_range.insert(0, '...')
    if page_range[-1] < paginator.num_pages:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    # 获取博客分类的对应博客数量
    # blog_type_list = list()
    # blog_types = BlogType.objects.all()
    # for blog_type in blog_types:
    #     blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
    #     blog_type_list.append(blog_type)
    blog_types = BlogType.objects.annotate(blog_count=Count('blog'))
    # 获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('created_time', 'month', order="DESC")
    blog_dates_dict = dict()
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(
            created_time__year=blog_date.year, created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count
    context = dict()
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = blog_types
    context['blog_dates'] = blog_dates_dict
    return context


def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request, blogs_all_list)
    # context['blogs_count'] = Blog.objects.all().count()
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request, blog)
    context = dict()
    context['blog'] = blog
    # 上一篇
    context['previous_blog'] = Blog.objects.filter(
        created_time__gt=blog.created_time).last()
    # 下一篇
    context['next_blog'] = Blog.objects.filter(
        created_time__lt=blog.created_time).first()
    response = render(request, 'blog/blog_detail.html', context)
    # 阅读cookie标记
    response.set_cookie(read_cookie_key, 'true')
    return response


def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blog_type'] = blog_type
    return render(request, 'blog/blog_with_type.html', context)


def blog_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(
        created_time__year=year, created_time__month=month)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blog_with_date'] = '%s年%s月' % (year, month)
    return render(request, 'blog/blog_with_date.html', context)
