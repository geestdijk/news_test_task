from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify


class New(models.Model):
    """A model for the handling News objects"""
    user = models.ForeignKey(
        get_user_model(), related_name="news", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True, auto_created=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'news'
        verbose_name = 'New'
        verbose_name_plural = 'News'
