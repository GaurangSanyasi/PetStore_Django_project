# Generated by Django 5.0 on 2024-01-08 08:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petApp', '0005_cart_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('flat', models.CharField(max_length=300, null=True)),
                ('landmark', models.CharField(max_length=200, null=True)),
                ('city', models.CharField(max_length=200, null=True)),
                ('state', models.CharField(max_length=100, null=True)),
                ('pincode', models.IntegerField(null=True)),
                ('contact', models.BigIntegerField(null=True)),
                ('contactA', models.BigIntegerField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]