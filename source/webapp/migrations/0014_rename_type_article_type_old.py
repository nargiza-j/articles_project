# Generated by Django 4.0 on 2022-01-26 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0013_article_status_article_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='type',
            new_name='type_old',
        ),
    ]
