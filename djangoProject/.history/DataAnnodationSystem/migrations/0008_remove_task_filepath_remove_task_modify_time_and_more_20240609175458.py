# Generated by Django 5.0.1 on 2024-06-09 09:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "DataAnnodationSystem",
            "0007_remove_task_filepath_remove_task_modify_time_and_more",
        ),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name="task",
        #     name="filePath",
        # ),
        migrations.RemoveField(
            model_name="task",
            name="modify_time",
        ),
        migrations.AddField(
            model_name="task",
            name="modifyTime",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
