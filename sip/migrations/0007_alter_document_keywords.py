# Generated by Django 4.2.7 on 2023-11-20 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sip', '0006_document_keywords'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='keywords',
            field=models.TextField(blank=True, null=True, verbose_name='Keywords'),
        ),
    ]
