import uuid

from django.db import models

from mptt.models import MPTTModel, TreeForeignKey


class Channel(models.Model):
    name = models.CharField(max_length=40, unique=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False)


class Category(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey(
        'self', null=True, related_name='children', db_index=True)
    channel = models.ForeignKey('category.Channel', on_delete=models.CASCADE)
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
