# Generated by Django 4.2.11 on 2024-03-31 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediwhistle', '0004_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='new', max_length=20),
        ),
    ]
