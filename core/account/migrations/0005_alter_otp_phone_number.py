# Generated by Django 5.0.7 on 2024-07-25 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_otp_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='phone_number',
            field=models.CharField(max_length=11, unique=True),
        ),
    ]
