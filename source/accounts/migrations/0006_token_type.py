# Generated by Django 4.0 on 2022-03-16 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_rename_emailconfirmationtoken_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='type',
            field=models.CharField(choices=[('email-confirmation', 'Email confirmation'), ('reset-password', 'Reset password')], default='email-confirmation', max_length=255),
            preserve_default=False,
        ),
    ]
