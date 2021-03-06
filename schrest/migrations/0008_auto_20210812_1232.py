# Generated by Django 3.2.6 on 2021-08-12 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schrest', '0007_auto_20210811_1913'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collegiate',
            name='links',
        ),
        migrations.AddField(
            model_name='link',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schrest.collegiate'),
        ),
        migrations.AlterField(
            model_name='link',
            name='link_url',
            field=models.URLField(),
        ),
    ]
