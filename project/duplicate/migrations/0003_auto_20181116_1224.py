# Generated by Django 2.1 on 2018-11-16 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duplicate', '0002_auto_20181116_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='user_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='lead',
            name='RPODescription',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='الوصف'),
        ),
    ]