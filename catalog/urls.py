from django.urls import path

from catalog.apps import MainConfig
from catalog.views import ProductListView, ProductDetailView, ContactCreateView, BlogListView, BlogCreateView, \
    BlogDetailView, BlogUpdateView, BlogDeleteView, toggle_public, DraftBlogListView, ProductCreateView, \
    ProductUpdateView

app_name = MainConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contact_create/', ContactCreateView.as_view(), name='contact_create'),
    path('view/<int:pk>/', ProductDetailView.as_view(), name='product_view'),
    path('create_product/', ProductCreateView.as_view(), name='create_product'),
    path('update_product/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('blogs/', BlogListView.as_view(), name='blogs'),
    path('create_blog/', BlogCreateView.as_view(), name='create_blog'),
    path('read_blog/<int:pk>/', BlogDetailView.as_view(), name='read_blog'),
    path('update_blog/<int:pk>/', BlogUpdateView.as_view(), name='update_blog'),
    path('delete_blog/<int:pk>/', BlogDeleteView.as_view(), name='delete_blog'),
    path('toggle_public/<int:pk>/', toggle_public, name='toggle_public'),
    path('drafts/', DraftBlogListView.as_view(), name='drafts'),
]
