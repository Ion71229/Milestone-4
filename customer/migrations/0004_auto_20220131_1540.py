# Generated by Django 3.2 on 2022-01-31 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20220131_1444'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordermodel',
            name='zip_code',
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='post_code',
            field=models.CharField(blank=True, max_length=7),
        ),
    ]
