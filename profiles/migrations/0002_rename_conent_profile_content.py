# Generated by Django 3.2.13 on 2022-05-26 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='conent',
            new_name='content',
        ),
    ]
