# Generated by Django 4.1.2 on 2022-12-09 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ordering', '0004_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order_User',
            fields=[
                ('order_id', models.IntegerField(primary_key=True, serialize=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ordering.user')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=10)),
                ('quantity', models.IntegerField()),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ordering.food')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ordering.order_user')),
            ],
        ),
    ]
