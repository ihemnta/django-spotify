# Generated by Django 2.1.7 on 2019-11-13 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mood', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mood_name', models.CharField(max_length=50)),
                ('mood_des', models.CharField(default='This is a Default Mood!', max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Moods',
        ),
    ]
