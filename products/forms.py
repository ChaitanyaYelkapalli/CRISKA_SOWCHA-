from django import forms
from django.forms import inlineformset_factory
from .models import Product, ProductColor


class ProductForm(forms.ModelForm):

    sizes = forms.MultipleChoiceField(
        choices=Product.SIZE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Product
        fields = [
            'name',
            'category',
            'price',
            'description',
            'main_image',
            'sizes',
            'material'
        ]

    def clean_sizes(self):
        sizes = self.cleaned_data.get('sizes')
        return ",".join(sizes) if sizes else ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk and self.instance.sizes:
            self.initial['sizes'] = self.instance.sizes.split(',')


class ProductColorForm(forms.ModelForm):

    class Meta:
        model = ProductColor
        fields = ['color_name', 'color_image']


ProductColorFormSetAdd = inlineformset_factory(
    Product,
    ProductColor,
    form=ProductColorForm,
    extra=1,
    can_delete=False
)


ProductColorFormSetEdit = inlineformset_factory(
    Product,
    ProductColor,
    form=ProductColorForm,
    extra=0,
    can_delete=True
)