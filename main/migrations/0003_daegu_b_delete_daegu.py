# Generated by Django 4.1 on 2023-04-20 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_alter_sejong_table"),
    ]

    operations = [
        migrations.CreateModel(
            name="Daegu_b",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.TextField(null=True)),
                ("cate1", models.TextField(null=True)),
                ("cate2", models.TextField(null=True)),
                ("cate3", models.TextField(null=True)),
                ("catemix", models.TextField(null=True)),
                ("lon", models.FloatField(null=True)),
                ("lat", models.FloatField(null=True)),
                ("type", models.TextField(null=True)),
                ("star", models.FloatField(null=True)),
                ("qty", models.TextField(null=True)),
                ("keyword", models.TextField(null=True)),
                ("review", models.TextField(null=True)),
                ("positive", models.TextField(null=True)),
            ],
            options={
                "db_table": "Daegu_b",
                "managed": False,
            },
        ),
        migrations.DeleteModel(
            name="Daegu",
        ),
    ]
