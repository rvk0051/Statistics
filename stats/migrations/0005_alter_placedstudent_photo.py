# Generated by Django 5.1.4 on 2025-03-06 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0004_alter_placedstudent_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placedstudent',
            name='photo',
            field=models.ImageField(blank=True, default='media/achievers/Designer(1).png', null=True, upload_to='media/achievers/'),
        ),
    ]
