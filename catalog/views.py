from django.shortcuts import get_object_or_404, redirect
from pytils.translit import slugify
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.models import Product, Buyer, Blog


class ContactCreateView(CreateView):
    model = Buyer
    fields = ('name', 'phone', 'message',)
    success_url = reverse_lazy('catalog:home')


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product


class BlogListView(ListView):
    model = Blog

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'text', 'avatar',)
    success_url = reverse_lazy('catalog:blogs')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'text', 'avatar',)

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:read_blog', args=[self.kwargs.get('pk')])


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blogs')


def toggle_public(request, pk):
    blog_item = get_object_or_404(Blog, pk=pk)
    if blog_item.is_published:
        blog_item.is_published = False
    else:
        blog_item.is_published = True
    blog_item.save()
    return redirect(reverse('catalog:blogs'))


class DraftBlogListView(ListView):
    model = Blog

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=False)
        return queryset
