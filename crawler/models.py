from django.contrib.postgres.fields import JSONField
from django.db import models

from crawler.constances import SCRIPT_CRAWLER_CHOICES


class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Product(BaseModel):

    product_id = models.CharField(max_length=500, unique=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    country_origin = models.CharField(max_length=500, null=True, blank=True)
    url = models.CharField(max_length=500, null=True, blank=True)
    price = models.FloatField(null=True)
    rating = models.PositiveSmallIntegerField(null=True)
    package_type = models.CharField(max_length=500, null=True, blank=True)
    type = models.CharField(max_length=500, null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    meta = JSONField(default=dict)

    def __str__(self):
        return self.product_id

class Site(BaseModel):

    url = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    script = models.CharField(max_length=500, choices=SCRIPT_CRAWLER_CHOICES)


class Category(BaseModel):

    url = models.CharField(max_length=500, null=True, blank=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    category_id = models.CharField(max_length=500, null=True, blank=True)
    site = models.ForeignKey('Site', on_delete=models.CASCADE)
    meta = JSONField(default=dict)

