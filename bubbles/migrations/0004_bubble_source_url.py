# Generated by Django 2.1.7 on 2019-03-09 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bubbles', '0003_auto_20190309_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='bubble',
            name='source_url',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
