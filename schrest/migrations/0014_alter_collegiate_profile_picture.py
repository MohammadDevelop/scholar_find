# Generated by Django 3.2.6 on 2021-08-13 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schrest', '0013_alter_collegiate_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collegiate',
            name='profile_picture',
            field=models.CharField(blank=True, default='/images/scholar.png', max_length=255, null=True),
        ),
    ]
