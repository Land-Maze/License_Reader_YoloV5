# Generated by Django 4.0.6 on 2022-11-07 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_license_last_seen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='license_detect',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]