# Generated by Django 3.0.6 on 2020-05-28 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_admin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hashtags',
            name='text',
            field=models.CharField(max_length=20),
        ),
    ]
