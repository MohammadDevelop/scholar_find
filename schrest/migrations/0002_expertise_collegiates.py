# Generated by Django 3.2.6 on 2021-08-09 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schrest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expertise',
            name='collegiates',
            field=models.ManyToManyField(to='schrest.Collegiate'),
        ),
    ]