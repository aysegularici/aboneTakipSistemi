# Generated by Django 4.0.6 on 2022-09-12 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aboneApp', '0002_alter_turnikeid_turnikeadi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turnikeid',
            name='turnikeAdi',
            field=models.CharField(max_length=20),
        ),
    ]
