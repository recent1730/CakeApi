# Generated by Django 3.1.3 on 2021-04-26 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cakeapi', '0006_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cakeid', models.IntegerField(default='')),
                ('name', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('image', models.ImageField(default='', upload_to='cake/images')),
                ('weight', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
    ]
