from django.db import models
from django.urls import reverse


class Document(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    text = models.TextField(blank=True, verbose_name='Text')
    description = models.TextField(blank=True, verbose_name='f')
    author = models.CharField(blank=True, max_length=70, verbose_name='Автор')
    url = models.CharField(max_length=200)
    time_publish = models.DateTimeField(auto_now_add=True)
    cover = models.ImageField(upload_to="cover", default='cover/image.png')
    essay = models.TextField(blank=True, verbose_name='Essay')
    keywords = models.TextField(blank=True, null=True, default=None, verbose_name='Keywords')
    terms = None

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('main_page')
