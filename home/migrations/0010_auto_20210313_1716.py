# Generated by Django 3.1.7 on 2021-03-13 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20210312_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.CharField(default='Post-Url-BlogPost-86771', max_length=80),
        ),
    ]
