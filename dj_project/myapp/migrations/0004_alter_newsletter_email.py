# Generated by Django 5.0.3 on 2024-03-09 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_newsletter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='email',
            field=models.EmailField(default='none', max_length=254),
        ),
    ]
