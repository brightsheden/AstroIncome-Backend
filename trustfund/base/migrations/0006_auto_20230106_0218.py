# Generated by Django 3.1.2 on 2023-01-06 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20230106_0217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='endAt',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
