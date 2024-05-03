from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect
from pytils.translit import slugify
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm, ProductModeratorForm
from catalog.models import Product, Buyer, Blog, Version, Category
from catalog.services import get_categories_from_cache


class ContactCreateView(CreateView):
    """Контроллер для страницы "Контакты"
    и сбор информации о неавторизованного пользователя, который оставил вопрос"""
    model = Buyer
    fields = ('name', 'phone', 'message',)
    success_url = reverse_lazy('catalog:home')


class CategoryListView(ListView):
    """Ппросмотр списка категорий товаров"""
    model = Category

    def get_queryset(self):
        return get_categories_from_cache()


class ProductListView(ListView):
    """Ппросмотр списка товаров"""
    model = Product


class ProductDetailView(DetailView):
    """Просмотр информации о конкретном товаре"""
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание нового товара"""
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')
    redirect_field_name = "catalog:create_product"

    def form_valid(self, form):
        """Присвоение товара создавшему его пользователю"""
        product = form.save()
        user = self.request.user
        product.user = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование товара"""
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        """Переброс после редактирования на страницу того же товара"""
        return reverse('catalog:product_view', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        """Добавление формы для редактирования версии товара"""
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            formset = VersionFormset(self.request.POST, instance=self.object)
        else:
            formset = VersionFormset(instance=self.object)
        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        """"""
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid:
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

    def get_form_class(self):
        """Отображение форм для пользователей с разными правами"""
        user = self.request.user
        if user == self.object.user or user.is_superuser:
            return ProductForm
        if user.has_perm('catalog.can_cancel_publication') and user.has_perm('catalog.can_change_description') and user.has_perm('catalog.can_change_category'):
            return ProductModeratorForm
        raise PermissionDenied


class BlogListView(ListView):
    """Просмотр списка новостей"""
    model = Blog

    def get_queryset(self):
        """Для отображения новостей только с признаком is_published(опубликованных)"""
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Создание новости"""
    model = Blog
    fields = ('title', 'text', 'avatar',)
    success_url = reverse_lazy('catalog:blogs')
    permission_required = 'catalog.add_blog'

    def form_valid(self, form):
        """создание slug"""
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Редактирование новости"""
    model = Blog
    fields = ('title', 'text', 'avatar',)
    permission_required = 'catalog.change_blog'

    def form_valid(self, form):
        """создание slug"""
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        """Переброс после редактирования на страницу той же новости"""
        return reverse('catalog:read_blog', args=[self.kwargs.get('pk')])


class BlogDetailView(DetailView):
    """Просмотр конкретной новости"""
    model = Blog

    def get_object(self, queryset=None):
        """Счетчик просмотров"""
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление новости"""
    model = Blog
    permission_required = 'catalog.delete_blog'
    success_url = reverse_lazy('catalog:blogs')


def toggle_public(pk):
    """Смена статуса блога опубликован/не опубликован"""
    blog_item = get_object_or_404(Blog, pk=pk)
    if blog_item.is_published:
        blog_item.is_published = False
    else:
        blog_item.is_published = True
    blog_item.save()
    return redirect(reverse('catalog:blogs'))


class DraftBlogListView(ListView):
    """Просмотр списка черновиков (статус is_published = False)"""
    model = Blog

    def get_queryset(self):
        """Выборка новостей со статусом False"""
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=False)
        return queryset
