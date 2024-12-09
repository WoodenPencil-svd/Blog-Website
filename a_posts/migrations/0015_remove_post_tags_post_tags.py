# Generated by Django 5.1.3 on 2024-12-09 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("a_posts", "0014_remove_post_tags_post_tags"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="tags",
        ),
        migrations.AddField(
            model_name="post",
            name="tags",
            field=models.ManyToManyField(related_name="posts", to="a_posts.tag"),
        ),
    ]
