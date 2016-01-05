# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SimulatorTestItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('test_time', models.DateTimeField(verbose_name='When Did The Test')),
                ('test_type', models.CharField(verbose_name='Test Type(eg: L3, MCU, LSU etc.)', max_length=20)),
                ('test_configuration', models.CharField(verbose_name='Test Configuration', max_length=50)),
                ('test_software', models.CharField(verbose_name='Tool for Test(eg: SpecCPU, Oprofile)', max_length=20)),
                ('test_item_IPC', models.FloatField(verbose_name='IPC Value', default=-9.99)),
                ('test_item_memory_bandwidth', models.FloatField(verbose_name='Memory Bandwidth(MB/s)', default=-9.99)),
                ('test_item_L1_miss_rate', models.FloatField(verbose_name='L1 Miss Rate(%)', default=-9.99)),
                ('test_item_reversed_one', models.FloatField(verbose_name='1st Reversed Item', default=-9.99)),
                ('test_item_reversed_two', models.FloatField(verbose_name='2nd Reversed Item', default=-9.99)),
                ('test_item_reversed_three', models.FloatField(verbose_name='3th Reversed Item', default=-9.99)),
            ],
        ),
        migrations.CreateModel(
            name='SimulatorTestResult',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('test_user', models.CharField(verbose_name='Test User', max_length=30)),
                ('test_comment', models.CharField(verbose_name='Test Comment', max_length=100)),
                ('test_record_time', models.DateTimeField(verbose_name='Record Test Result Time', default=django.utils.timezone.now)),
                ('test_result_detail_link', models.URLField(verbose_name='Test Result URL', max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='UploadFilename',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('test_user', models.CharField(verbose_name='Test User', max_length=30)),
                ('test_comment', models.CharField(verbose_name='Test Comment', max_length=100)),
                ('test_record_time', models.DateTimeField(verbose_name='Record Test Result Time')),
                ('filename', models.FileField(upload_to='%Y-%m-%d/%H-%M-%S')),
                ('test_result_detail_link', models.URLField(verbose_name='Test Result URL', max_length=300)),
            ],
        ),
        migrations.AddField(
            model_name='simulatortestitem',
            name='test_result',
            field=models.ForeignKey(to='simulator.SimulatorTestResult'),
        ),
    ]
