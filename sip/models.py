from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=200)
    file_path = models.FileField(upload_to='documents/')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    text = models.TextField(blank=True, verbose_name='Описание')
    some_info = models.TextField(blank=True, verbose_name='f')
    author = models.CharField(max_length=70, verbose_name='Автор')
    time_publish = models.DateTimeField(auto_now_add=True)
    cover = models.ImageField(upload_to="cover")
    terms = None

    def __str__(self):
        return self.title

# class Keyword(models.Model):
#     document = models.ForeignKey(Document, on_delete=models.CASCADE)
#     file_path = models.FileField(upload_to='keywords/')
#
#
# class QualityMetric(models.Model):
#     file_path = models.FileField(upload_to='metrics/')
