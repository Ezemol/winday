# Generated by Django 5.0.6 on 2024-10-12 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('winday', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='winday_user_groups', to='auth.group', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='winday_user_permissions', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AlterModelTable(
            name='user',
            table='winday_user',
        ),
    ]
