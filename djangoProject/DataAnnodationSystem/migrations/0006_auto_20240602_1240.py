# Generated by Django 2.1.7 on 2024-06-02 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DataAnnodationSystem', '0005_auto_20240602_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='headSculpturePath',
            field=models.CharField(default='/static/images/ico_uer.gif', max_length=200),
        ),
    ]
