# Generated by Django 3.0.4 on 2020-03-16 20:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('examenes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='examen',
            old_name='alumno',
            new_name='creador',
        ),
        migrations.RemoveField(
            model_name='examen',
            name='calificacion',
        ),
        migrations.RemoveField(
            model_name='examen',
            name='data',
        ),
    ]
