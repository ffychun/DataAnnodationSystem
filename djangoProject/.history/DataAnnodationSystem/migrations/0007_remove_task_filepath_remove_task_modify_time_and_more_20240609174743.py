# Generated by Django 5.0.1 on 2024-06-09 09:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("DataAnnodationSystem", "0006_auto_20240602_1240"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="task",
            name="modify_time",
        ),
        migrations.AlterField(
            model_name="order",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="headSculpturePath",
            field=models.CharField(default="static/images/ico_uer.gif", max_length=200),
        ),
    ]
