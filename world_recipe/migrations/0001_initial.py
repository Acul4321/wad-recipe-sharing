# Generated by Django 5.1.7 on 2025-03-21 16:58

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Recipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "originID",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MaxValueValidator(177),
                            django.core.validators.MinValueValidator(0),
                        ]
                    ),
                ),
                (
                    "meal_type",
                    models.CharField(
                        choices=[
                            ("BF", "Breakfast"),
                            ("LU", "Lunch"),
                            ("DN", "Dinner"),
                            ("SN", "Snack"),
                            ("DS", "Dessert"),
                        ],
                        max_length=2,
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="recipe_images/"
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                (
                    "publish_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("ingredients", models.TextField()),
                ("instructions", models.TextField()),
                ("slug", models.SlugField(unique=True)),
                (
                    "authorID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Rating",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "rating",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MaxValueValidator(5),
                            django.core.validators.MinValueValidator(0),
                        ]
                    ),
                ),
                (
                    "userID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "recipeID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="world_recipe.recipe",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DateTimeField(default=django.utils.timezone.now)),
                ("content", models.TextField(max_length=2000)),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="world_recipe.comment",
                    ),
                ),
                (
                    "userID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "recipeID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="world_recipe.recipe",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "originID",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MaxValueValidator(177),
                            django.core.validators.MinValueValidator(0),
                        ]
                    ),
                ),
                (
                    "profile_picture",
                    models.ImageField(
                        default="profile_pictures/default.jpg",
                        upload_to="profile_pictures",
                    ),
                ),
                ("description", models.TextField(blank=True, max_length=500)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
