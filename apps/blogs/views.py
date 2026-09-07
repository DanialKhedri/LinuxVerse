from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post, Category


def post_list(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    selected_category = None
    
    context = {
        'posts': page_obj,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'blogs/post_list.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    
    prev_post = Post.objects.filter(
        is_published=True, 
        created_at__lt=post.created_at
    ).order_by('-created_at').first()
    
    next_post = Post.objects.filter(
        is_published=True, 
        created_at__gt=post.created_at
    ).order_by('created_at').first()
    
    context = {
        'post': post,
        'prev_post': prev_post,
        'next_post': next_post,
    }
    return render(request, 'blogs/post_detail.html', context)