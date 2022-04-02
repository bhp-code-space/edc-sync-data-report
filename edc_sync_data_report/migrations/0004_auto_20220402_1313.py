# Generated by Django 3.2.11 on 2022-04-02 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edc_sync_data_report', '0003_auto_20220402_1248'),
    ]

    operations = [
        migrations.RenameField(
            model_name='syncmodels',
            old_name='cls_name',
            new_name='model_name',
        ),
        migrations.AddField(
            model_name='syncmodels',
            name='app_label',
            field=models.CharField(default='', max_length=100, verbose_name='App label'),
            preserve_default=False,
        ),
    ]
