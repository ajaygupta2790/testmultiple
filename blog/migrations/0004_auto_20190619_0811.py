# Generated by Django 2.0.13 on 2019-06-19 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20190618_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='rating_dislikes',
            field=models.PositiveIntegerField(blank=True, default=0, editable=False),
        ),
        migrations.AddField(
            model_name='comment',
            name='rating_likes',
            field=models.PositiveIntegerField(blank=True, default=0, editable=False),
        ),
        migrations.AddField(
            model_name='post',
            name='rating_dislikes',
            field=models.PositiveIntegerField(blank=True, default=0, editable=False),
        ),
        migrations.AddField(
            model_name='post',
            name='rating_likes',
            field=models.PositiveIntegerField(blank=True, default=0, editable=False),
        ),
    ]