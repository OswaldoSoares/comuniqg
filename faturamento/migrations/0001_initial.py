# Generated by Django 3.1.3 on 2022-12-07 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fatura',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fatura', models.IntegerField(default=0)),
            ],
        ),
    ]