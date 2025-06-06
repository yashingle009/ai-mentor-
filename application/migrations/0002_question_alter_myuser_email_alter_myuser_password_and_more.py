# Generated by Django 4.2.9 on 2024-02-27 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='question',
            fields=[
                ('que', models.CharField(max_length=200, null=True)),
                ('answer', models.CharField(max_length=1000, null=True)),
                ('uid', models.IntegerField(null=True)),
                ('rid', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.AlterField(
            model_name='myuser',
            name='email',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='password',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='username',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
