from django.contrib import admin
from django.utils.html import format_html

from crawler.models import Site, Category, Product

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):

    list_display = ('title', 'url', 'script')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('title', 'url', 'category_id', 'site', 'product_count')

    def product_count(self, obj):
        return Product.objects.filter(category=obj).count()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_per_page = 20
    list_display = ('product_id', 'title', 'image', 'price', 'category', 'updated_at')

    def image(self, obj):
        image_url = obj.meta['image']
        href_url = obj.url or '#'
        return format_html(f"<a target='_blank' href='{href_url}'><img height=100 src='{image_url}'/></a>")
