# Generated by Django 2.1.1 on 2019-07-22 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='financialinfo',
            name='slug',
            field=models.SlugField(allow_unicode=True, default='djangodbmodelsquery_utilsdeferredattribute-object-at-0x000002155a8b0e48', unique=True),
        ),
    ]
