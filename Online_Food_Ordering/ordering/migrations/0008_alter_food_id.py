# Generated by Django 4.1.2 on 2022-12-10 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordering', '0007_alter_order_user_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
