# Generated by Django 2.0.8 on 2018-11-16 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duplicate', '0010_auto_20181116_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='employee',
            field=models.ManyToManyField(blank=True, to='duplicate.Employee'),
        ),
    ]
