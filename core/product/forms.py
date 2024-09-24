from django import forms
from .models import Product, Category, ProductVariant
from django_jsonform.widgets import JSONFormWidget


class ProductCreationForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.filter(sub_categories__isnull=True))

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        product = self.instance
        if not product.category_id:
            self.fields['attributes'].widget.input_type = 'hidden'
        else:
            self.fields['attributes'].widget = JSONFormWidget(schema=product.category.product_attrs_schema)


class ProductVariantCreationForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        product_variant = self.instance
        if not product_variant.product_id:
            self.fields['attributes'].widget.input_type = 'hidden'
        else:
            self.fields['attributes'].widget = JSONFormWidget(
                schema=product_variant.product.category.variant_attrs_schema)
