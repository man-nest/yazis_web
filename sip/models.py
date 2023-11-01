from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=200)
    file_path = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.title


class Keyword(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    file_path = models.FileField(upload_to='keywords/')


class QualityMetric(models.Model):
    file_path = models.FileField(upload_to='metrics/')
