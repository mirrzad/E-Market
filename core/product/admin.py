from django.contrib import admin
from .models import Category, Product, ProductVariant
from django.db.models import JSONField
from jsoneditor.forms import JSONEditor
from .forms import ProductCreationForm, ProductVariantCreationForm


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'parent')
    list_filter = [('parent', admin.RelatedOnlyFieldListFilter)]
    search_fields = ('title', 'slug')
    ordering = ('title',)
    formfield_overrides = {JSONField: {'widget': JSONEditor(
        init_options={"mode": "code", "modes": ["view", "code", "tree"]},
    )}}


class ProductVariantInline(admin.StackedInline):
    model = ProductVariant
    form = ProductVariantCreationForm
    formfield_overrides = {JSONField: {'widget': JSONEditor(
        init_options={"mode": "code", "modes": ["view", "code", "tree"]},
    )}}


class ProductAdmin(admin.ModelAdmin):
    form = ProductCreationForm

    list_display = ('title', 'category')
    list_filter = [('category', admin.RelatedOnlyFieldListFilter)]
    search_fields = ('title', 'category__title')
    ordering = ('category',)
    formfield_overrides = {JSONField: {'widget': JSONEditor(
        init_options={"mode": "code", "modes": ["view", "code", "tree"]},
    )}}

    inlines = [ProductVariantInline]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
