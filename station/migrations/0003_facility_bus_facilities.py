# Generated by Django 4.2.1 on 2023-06-17 10:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "station",
            "0002_order_trip_ticket_trip_station_tri_source_1ae98f_idx_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Facility",
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
                ("name", models.CharField(max_length=63)),
            ],
        ),
        migrations.AddField(
            model_name="bus",
            name="facilities",
            field=models.ManyToManyField(related_name="buses", to="station.facility"),
        ),
    ]
