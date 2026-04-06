from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from products import views

urlpatterns = [

    # Django default admin (optional)
    path('admin/', admin.site.urls),

    # ------------------------------
    # CUSTOM ADMIN LOGIN SYSTEM
    # ------------------------------
    path('admin-login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    # ------------------------------
    # DASHBOARD
    # ------------------------------
    path('dashboard/', views.dashboard, name='dashboard'),
    path('category/<str:category>/', views.category_products, name='category_products'),

    # ------------------------------
    # PRODUCT MANAGEMENT
    # ------------------------------
    path('add-product/', views.add_product, name='add_product'),
    path('edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add-to-wishlist/<int:pk>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:pk>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    # ------------------------------
    # TRASH MANAGEMENT
    # ------------------------------
    path('trash/', views.trash, name='trash'),
    path('restore/<int:pk>/', views.restore_product, name='restore_product'),
    path('permanent-delete/<int:pk>/', views.permanent_delete, name='permanent_delete'),
    path('bulk-delete/', views.bulk_permanent_delete, name='bulk_delete'),

    # ------------------------------
    # FRONTEND WEBSITE
    # ------------------------------
    path('', views.home, name='home'),
]

# Media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)