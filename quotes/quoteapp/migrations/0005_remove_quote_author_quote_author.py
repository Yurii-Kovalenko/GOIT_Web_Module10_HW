# Generated by Django 5.0.3 on 2024-03-15 18:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quoteapp", "0004_alter_author_born_date"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="quote",
            name="author",
        ),
        migrations.AddField(
            model_name="quote",
            name="author",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="quoteapp.author",
            ),
        ),
    ]