# Generated by Django 4.2 on 2023-04-26 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='service',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
