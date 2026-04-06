from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from .models import Product
from .forms import (
    ProductForm,
    ProductColorFormSetAdd,
    ProductColorFormSetEdit
)




# ADMIN DASHBOARD
@login_required
def dashboard(request):
    products = Product.objects.filter(is_archived=False).order_by('-created_at')
    return render(request, 'dashboard.html', {'products': products})

from django.shortcuts import render
from .models import Product

def dashboard(request):
    products = Product.objects.filter(is_archived=False).order_by('-created_at')

    context = {
        "products": products,
        "total_products": products.count(),
        "designer_count": products.filter(category="designer").count(),
        "regular_count": products.filter(category="regular").count(),
        "casual_count": products.filter(category="casual").count(),
    }

    return render(request, "dashboard.html", context)

# CUSTOM LOGIN VIEW
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, 'already_logged_in.html')
        return super().dispatch(request, *args, **kwargs)


# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')


# ADD PRODUCT
@login_required
def add_product(request):

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        formset = ProductColorFormSetAdd(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            product = form.save()
            formset.instance = product
            formset.save()
            return redirect('dashboard')
    else:
        form = ProductForm()
        formset = ProductColorFormSetAdd()

    return render(request, 'product_form.html', {
        'form': form,
        'formset': formset,
        'is_edit': False
    })

def category_products(request, category):
    products = Product.objects.filter(category=category, is_archived=False)
    wishlist = request.session.get('wishlist', [])

    return render(request, 'home.html', {
        'products': products,
        'category': category,
        'wishlist': wishlist
    })
# EDIT PRODUCT
@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ProductColorFormSetEdit(request.POST, request.FILES, instance=product)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('dashboard')
    else:
        form = ProductForm(instance=product)
        formset = ProductColorFormSetEdit(instance=product)

    return render(request, 'product_form.html', {
        'form': form,
        'formset': formset,
        'is_edit': True
    })


# DELETE (SOFT DELETE → TRASH)
@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('dashboard')


# TRASH PAGE
@login_required
def trash(request):
    products = Product.objects.filter(is_archived=True)
    return render(request, 'trash.html', {'products': products})


# RESTORE PRODUCT
@login_required
def restore_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.is_archived = False
    product.archived_date = None
    product.save()
    return redirect('trash')


# PERMANENT DELETE
@login_required
def permanent_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.hard_delete()
    return redirect('trash')


# BULK PERMANENT DELETE
@login_required
def bulk_permanent_delete(request):
    if request.method == "POST":
        ids = request.POST.getlist('selected_products')
        products = Product.objects.filter(id__in=ids)

        for product in products:
            product.hard_delete()

    return redirect('trash')

from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_archived=False)
    colors = product.color_variants.all()
    wishlist = request.session.get('wishlist', [])

    # ✅ Split sizes safely
    size_list = []
    if product.sizes:
        size_list = [size.strip() for size in product.sizes.split(',')]

    return render(request, 'product_detail.html', {
        'product': product,
        'colors': colors,
        'wishlist': wishlist,
        'size_list': size_list,   # 👈 send to template
    })
from django.shortcuts import get_object_or_404
from .models import Product


def add_to_wishlist(request, pk):
    wishlist = request.session.get('wishlist', [])

    if pk not in wishlist:
        wishlist.append(pk)

    request.session['wishlist'] = wishlist
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def remove_from_wishlist(request, pk):
    wishlist = request.session.get('wishlist', [])

    if pk in wishlist:
        wishlist.remove(pk)

    request.session['wishlist'] = wishlist
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def wishlist(request):
    wishlist = request.session.get('wishlist', [])
    products = Product.objects.filter(id__in=wishlist, is_archived=False)

    return render(request, 'wishlist.html', {'products': products})


from django.db.models import Q

def home(request):
    query = request.GET.get('q')
    products = Product.objects.filter(is_archived=False)

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(material__icontains=query)
        )

    wishlist = request.session.get('wishlist', [])

    return render(request, 'home.html', {
        'products': products,
        'wishlist': wishlist,
        'wishlist_count': len(wishlist)
    })