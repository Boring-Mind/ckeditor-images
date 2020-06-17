# Generated by Django 3.0.5 on 2020-05-08 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('description', models.CharField(max_length=300)),
                ('content', models.TextField()),
                ('post_date', models.DateField(auto_now_add=True)),
                ('preview_img_url', models.CharField(max_length=250)),
                ('post_status', models.CharField(choices=[('DR', 'Draft'), ('ST', 'Stash'), ('PB', 'Public')], default='DR', max_length=2)),
                ('hashtags', models.ManyToManyField(to='blog.Hashtags')),
            ],
            options={
                'ordering': ['post_date'],
            },
        ),
    ]