# Generated by Django 2.2.1 on 2019-08-13 08:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('joins', '0004_join_ref_id'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='join',
            unique_together={('email', 'ref_id')},
        ),
    ]