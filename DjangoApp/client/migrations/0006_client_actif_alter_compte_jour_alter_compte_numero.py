# Generated by Django 4.1.3 on 2022-11-20 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0005_alter_client_telephone_alter_compte_numero'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='actif',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='compte',
            name='jour',
            field=models.DateTimeField(null=True, verbose_name='Date de creation'),
        ),
        migrations.AlterField(
            model_name='compte',
            name='numero',
            field=models.IntegerField(max_length=11, verbose_name='Numero de compte'),
        ),
    ]
