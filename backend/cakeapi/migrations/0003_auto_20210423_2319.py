# Generated by Django 3.1.3 on 2021-04-23 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cakeapi', '0002_cakes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cakes',
            name='id',
        ),
        migrations.AlterField(
            model_name='cakes',
            name='cakeid',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]
