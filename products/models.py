from django.db import models
from django.utils import timezone


# ==========================================
# PRODUCT MODEL
# ==========================================
class Product(models.Model):

    CATEGORY_CHOICES = [
        ('designer', 'Designer Wear'),
        ('regular', 'Regular Wear'),
        ('casual', 'Casual Wear'),
    ]

    SIZE_CHOICES = [
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
    ]

    # ----------------------------
    # BASIC INFO
    # ----------------------------
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    # Main Product Image
    main_image = models.ImageField(upload_to='products/')

    # Sizes (stored as comma-separated text)
    sizes = models.CharField(
        max_length=100,
        blank=True,
        help_text="Select available sizes"
    )

    # Optional Material
    material = models.CharField(
        max_length=255,
        blank=True,
        help_text="Example: Cotton, Silk, Linen"
    )

    # ----------------------------
    # ARCHIVE SYSTEM
    # ----------------------------
    is_archived = models.BooleanField(default=False)
    archived_date = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # ----------------------------
    # SOFT DELETE (Move to Trash)
    # ----------------------------
    def delete(self, *args, **kwargs):
        self.is_archived = True
        self.archived_date = timezone.now()
        self.save()

    # ----------------------------
    # PERMANENT DELETE
    # ----------------------------
    def hard_delete(self):
        super().delete()

    def __str__(self):
        return self.name


# ==========================================
# COLOR VARIANT MODEL
# ==========================================
class ProductColor(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='color_variants'
    )

    color_name = models.CharField(max_length=100)
    color_image = models.ImageField(upload_to='products/colors/')

    def __str__(self):
        return f"{self.product.name} - {self.color_name}"