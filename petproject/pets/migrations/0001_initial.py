# Generated by Django 5.1.1 on 2024-10-05 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='pets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('breed', models.CharField()),
                ('gender', models.CharField()),
                ('image', models.ImageField(upload_to='pets/')),
            ],
        ),
    ]
