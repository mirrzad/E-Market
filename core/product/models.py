from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from jsonschema import validate
from django.core.exceptions import ValidationError


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    parent = models.ForeignKey('self', models.CASCADE, related_name='sub_categories', null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    product_attrs_schema = models.JSONField(default=dict, blank=True)
    variant_attrs_schema = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home:category-filter', args=[self.slug],)

    @property
    def is_leaf(self):
        return not self.sub_categories.exists()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    image = models.ImageField(upload_to='images/products', null=True, blank=True)
    description = RichTextUploadingField(null=True, blank=True)
    attributes = models.JSONField(default=dict, blank=True)
    is_available = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product:product-details', args=(self.slug,))

    def clean(self, *args, **kwargs):
        validate(instance=self.attributes, schema=self.category.product_attrs_schema)
        if not self.category.is_leaf:
            raise ValidationError({'category': f'{self.category} is not a leaf category.'})
        return super().clean()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.full_clean()
        return super().save(*args, **kwargs)


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    price = models.IntegerField(null=True, blank=True)
    item_count = models.IntegerField(null=True, blank=True)
    attributes = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.product.title

    def clean(self, *args, **kwargs):
        validate(instance=self.attributes, schema=self.product.category.variant_attrs_schema)
        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
