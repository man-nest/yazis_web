# Generated by Django 4.2.7 on 2023-11-19 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sip', '0004_document_essay_alter_document_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='some_info',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='document',
            name='file_path',
        ),
        migrations.AlterField(
            model_name='document',
            name='author',
            field=models.CharField(blank=True, max_length=70, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='document',
            name='text',
            field=models.TextField(blank=True, verbose_name='Text'),
        ),
    ]