from django.db import models
from django.urls import reverse


class Document(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    file_path = models.FileField(upload_to='documents/')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    text = models.TextField(blank=True, verbose_name='Описание')
    some_info = models.TextField(blank=True, verbose_name='f', default='No information')
    author = models.CharField(max_length=70, verbose_name='Автор', default='No information')
    time_publish = models.DateTimeField(auto_now_add=True)
    cover = models.ImageField(upload_to="cover", default='cover/image.png')
    terms = None

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('main_page')
