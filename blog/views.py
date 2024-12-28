from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Blog, Category, Tag, Comment
import bleach


def truncate_html(context, length):
    allow_tags = ['p', 'b', 'i', 'u', 'a', 'br', 'strong', 'em', 'code', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']

    truncated_context = bleach.clean(context, tags=allow_tags, strip=True)

    if len(truncated_context) > length:
        truncated_context = truncated_context[:length] + '...'
    return truncated_context


class BlogListView(ListView):
    model = Blog
    template_name = 'blog-list.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        blogs = Blog.objects.filter(status='published').order_by('-created_at')

        category_slug = self.request.GET.get('category')
        if category_slug:
            blogs = blogs.filter(categories__slug=category_slug)

        for i in blogs:
            i.truncated_content = truncate_html(i.content, 150)
        return blogs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Blog.objects.filter(status='published').order_by('-created_at')[:5]
        context['categories'] = Category.objects.order_by('name')
        context['tags'] = Tag.objects.order_by('name')
        return context

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog-detail.html'
    context_object_name = 'blog'

    def post(self, request, *args, **kwargs):
        blog = self.get_object()
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            Comment.objects.get(name=name, email=email, message=message)
            return redirect('blog-detail', slug=blog.slug)

    def get_queryset(self):
        return Blog.objects.filter(status='published')

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return self.get_queryset().get(slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Blog.objects.filter(status='published').order_by('-created_at')[:5]
        context['categories'] = Category.objects.order_by('name')
        context['tags'] = Tag.objects.order_by('name')
        context['comments'] = Comment.objects.filter(blog=self.object).order_by('-created_at')
        return context
