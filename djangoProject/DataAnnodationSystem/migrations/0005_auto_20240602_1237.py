# Generated by Django 2.1.7 on 2024-06-02 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DataAnnodationSystem', '0004_auto_20240602_0016'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='headSculpturePath',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
