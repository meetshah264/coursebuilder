# Generated by Django 3.2.3 on 2023-07-23 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursebuilder', '0009_auto_20230723_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='membership',
            field=models.CharField(choices=[('Bronze', 'Bronze'), ('Silver', 'Silver'), ('Gold', 'Gold')], default='B', max_length=10),
        ),
    ]
