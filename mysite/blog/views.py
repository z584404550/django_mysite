from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Blog, BlogType

# Create your views here.


def blog_list(request):
    blogs_all_list = Blog.objects.all()
    # 每10页进行分页
    paginator = Paginator(blogs_all_list, 10)
    # 获取页码参数（GET请求）
    page_num = request.GET.get('page', 1)
    page_of_blogs = paginator.get_page(page_num)

    context = dict()
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.all()
    # context['blogs_count'] = Blog.objects.all().count()
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, blog_pk):
    context = dict()
    context['blog'] = get_object_or_404(Blog, pk=blog_pk)
    return render(request, 'blog/blog_detail.html', context)


def blogs_with_type(request, blog_type_pk):
    context = dict()
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    context['blog_type'] = blog_type
    context['blogs'] = Blog.objects.filter(blog_type=blog_type)
    context['blog_types'] = BlogType.objects.all()
    return render(request, 'blog/blog_with_type.html', context)
