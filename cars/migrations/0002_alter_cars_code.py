# Generated by Django 5.1.1 on 2024-09-17 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cars',
            name='code',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
