# Generated by Django 3.2.11 on 2022-04-04 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edc_sync_data_report', '0005_auto_20220403_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='syncsite',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]