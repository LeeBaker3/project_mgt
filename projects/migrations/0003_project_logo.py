# Generated by Django 2.2.13 on 2020-06-15 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_deliverable'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='logo',
            field=models.ImageField(blank=True, upload_to='logos/'),
        ),
    ]