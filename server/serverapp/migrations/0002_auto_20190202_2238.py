# Generated by Django 2.1.4 on 2019-02-03 03:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('serverapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeetingMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='meeting',
            name='text',
            field=models.TextField(default='gay'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='meetingmember',
            name='meeting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serverapp.Meeting'),
        ),
        migrations.AddField(
            model_name='meetingmember',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serverapp.Profile'),
        ),
    ]
