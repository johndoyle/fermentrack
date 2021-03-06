# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-04-16 15:08
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [('gravity', '0001_initial'), ('gravity', '0002_tilt_refactor'), ('gravity', '0003_tiltbridge_mdns_id'), ('gravity', '0004_BrewersFriend_Support'), ('gravity', '0005_auto_20200416_1456')]

    initial = True

    dependencies = [
        ('app', '0007_auto_20171105_1523'),
    ]

    operations = [
        migrations.CreateModel(
            name='GravityLogPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gravity', models.DecimalField(decimal_places=11, help_text='The current (loggable) sensor gravity', max_digits=13)),
                ('temp', models.DecimalField(decimal_places=10, help_text='The current (loggable) temperature', max_digits=13, null=True)),
                ('temp_format', models.CharField(choices=[('C', 'Celsius'), ('F', 'Fahrenheit')], default='F', max_length=1)),
                ('temp_is_estimate', models.BooleanField(default=True, help_text='Is this temperature an estimate?')),
                ('extra_data', models.CharField(blank=True, help_text='Extra data/notes about this point', max_length=255, null=True)),
                ('log_time', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('gravity_latest', models.DecimalField(decimal_places=11, default=None, help_text='The latest gravity (without smoothing/filtering if applicable)', max_digits=13, null=True)),
                ('temp_latest', models.DecimalField(decimal_places=10, default=None, help_text='The latest temperature (without smoothing/filtering if applicable)', max_digits=13, null=True)),
            ],
            options={
                'ordering': ['log_time'],
                'verbose_name': 'Gravity Log Point',
                'managed': False,
                'verbose_name_plural': 'Gravity Log Points',
            },
        ),
        migrations.CreateModel(
            name='GravityLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('format', models.CharField(choices=[('C', 'Celsius'), ('F', 'Fahrenheit')], default='F', max_length=1)),
                ('model_version', models.IntegerField(default=1)),
                ('display_extra_data_as_annotation', models.BooleanField(default=False, help_text='Should any extra data be displayed as a graph annotation?')),
            ],
        ),
        migrations.CreateModel(
            name='GravitySensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Unique name for this device', max_length=48, unique=True)),
                ('temp_format', models.CharField(choices=[('C', 'Celsius'), ('F', 'Fahrenheit')], default='C', help_text='Temperature units', max_length=1)),
                ('sensor_type', models.CharField(choices=[('tilt', 'Tilt Hydrometer'), ('manual', 'Manual')], default='manual', help_text='Type of gravity sensor used', max_length=10)),
                ('status', models.CharField(choices=[('active', 'Active, Managed by Circus'), ('unmanaged', 'Active, NOT managed by Circus'), ('disabled', 'Explicitly disabled, cannot be launched'), ('updating', 'Disabled, pending an update')], default='active', help_text='Status of the gravity sensor (used by scripts that interact with it)', max_length=15)),
                ('active_log', models.ForeignKey(blank=True, default=None, help_text='The currently active log of readings', null=True, on_delete=django.db.models.deletion.CASCADE, to='gravity.GravityLog')),
                ('assigned_brewpi_device', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gravity_sensor', to='app.BrewPiDevice')),
            ],
            options={
                'verbose_name': 'Gravity Sensor',
                'verbose_name_plural': 'Gravity Sensors',
            },
        ),
        migrations.AddField(
            model_name='gravitylog',
            name='device',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gravity.GravitySensor'),
        ),
        migrations.CreateModel(
            name='TiltConfiguration',
            fields=[
                ('sensor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='tilt_configuration', serialize=False, to='gravity.GravitySensor')),
                ('color', models.CharField(choices=[('Black', 'Black'), ('Orange', 'Orange'), ('Green', 'Green'), ('Blue', 'Blue'), ('Purple', 'Purple'), ('Red', 'Red'), ('Yellow', 'Yellow'), ('Pink', 'Pink')], help_text='The color of Tilt Hydrometer being used', max_length=32, unique=True)),
                ('average_period_secs', models.IntegerField(default=120, help_text='Number of seconds over which to average readings')),
                ('median_window_vals', models.IntegerField(default=10000, help_text="Number of readings to include in the average window. If set to less than ~1.3*average_period_secs, you will get a moving average. If set to greater, you'll get the median value.")),
                ('polling_frequency', models.IntegerField(default=15, help_text='How frequently Fermentrack should update the temp/gravity reading from the sensor')),
                ('bluetooth_device_id', models.IntegerField(default=0, help_text='Almost always 0 - Change if you have Bluetooth issues')),
            ],
        ),
        migrations.CreateModel(
            name='TiltGravityCalibrationPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gravity.TiltConfiguration')),
                ('actual_gravity', models.DecimalField(decimal_places=3, default=1.0, max_digits=5, verbose_name='Actual (Correct) Gravity value')),
                ('tilt_measured_gravity', models.DecimalField(decimal_places=3, default=1.0, max_digits=5, verbose_name='Tilt Measured Gravity Value')),
            ],
        ),
        migrations.CreateModel(
            name='TiltTempCalibrationPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orig_value', models.DecimalField(decimal_places=4, help_text='Original (Sensor) Temp Value', max_digits=8, verbose_name='Original (Sensor) Temp Value')),
                ('actual_value', models.DecimalField(decimal_places=4, help_text='Actual (Measured) Temp Value', max_digits=8, verbose_name='Actual (Measured) Temp Value')),
                ('temp_format', models.CharField(choices=[('F', 'Fahrenheit'), ('C', 'Celsius')], default='F', max_length=1)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gravity.TiltConfiguration')),
            ],
        ),
        migrations.AlterField(
            model_name='gravitysensor',
            name='temp_format',
            field=models.CharField(choices=[('F', 'Fahrenheit'), ('C', 'Celsius')], default='F', help_text='Temperature units', max_length=1),
        ),
        migrations.CreateModel(
            name='IspindelConfiguration',
            fields=[
                ('sensor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='ispindel_configuration', serialize=False, to='gravity.GravitySensor')),
                ('name_on_device', models.CharField(help_text='The name configured on the iSpindel device itself', max_length=64, unique=True)),
                ('third_degree_coefficient', models.DecimalField(decimal_places=10, default=0.0, help_text='The third degree coefficient in the gravity conversion equation', max_digits=13)),
                ('second_degree_coefficient', models.DecimalField(decimal_places=10, default=0.0, help_text='The second degree coefficient in the gravity conversion equation', max_digits=13)),
                ('first_degree_coefficient', models.DecimalField(decimal_places=10, default=0.0, help_text='The first degree coefficient in the gravity conversion equation', max_digits=13)),
                ('constant_term', models.DecimalField(decimal_places=10, default=0.0, help_text='The constant term in the gravity conversion equation', max_digits=13)),
                ('coefficients_up_to_date', models.BooleanField(default=False, help_text='Have the calibration points changed since the coefficient calculator was run?')),
            ],
        ),
        migrations.CreateModel(
            name='IspindelGravityCalibrationPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('angle', models.DecimalField(decimal_places=7, max_digits=10, verbose_name='Angle (Measured by Device)')),
                ('gravity', models.DecimalField(decimal_places=4, max_digits=8, verbose_name='Gravity Value (Measured Manually)')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gravity.IspindelConfiguration')),
            ],
        ),
        migrations.AlterField(
            model_name='gravitysensor',
            name='sensor_type',
            field=models.CharField(choices=[('tilt', 'Tilt Hydrometer'), ('ispindel', 'iSpindel'), ('manual', 'Manual')], default='manual', help_text='Type of gravity sensor used', max_length=10),
        ),
        migrations.AlterField(
            model_name='ispindelconfiguration',
            name='constant_term',
            field=models.FloatField(default=0.0, help_text='The constant term in the gravity conversion equation'),
        ),
        migrations.AlterField(
            model_name='ispindelconfiguration',
            name='first_degree_coefficient',
            field=models.FloatField(default=0.0, help_text='The first degree coefficient in the gravity conversion equation'),
        ),
        migrations.AlterField(
            model_name='ispindelconfiguration',
            name='second_degree_coefficient',
            field=models.FloatField(default=0.0, help_text='The second degree coefficient in the gravity conversion equation'),
        ),
        migrations.AlterField(
            model_name='ispindelconfiguration',
            name='third_degree_coefficient',
            field=models.FloatField(default=0.0, help_text='The third degree coefficient in the gravity conversion equation'),
        ),
        migrations.CreateModel(
            name='TiltBridge',
            fields=[
                ('name', models.CharField(help_text='Name to identify this TiltBridge', max_length=64)),
                ('mdns_id', models.CharField(help_text="mDNS ID used by the TiltBridge to identify itself both on your network and to Fermentrack. NOTE - Prefix only - do not include '.local'", max_length=64, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(regex='^[a-zA-Z0-9]+$')])),
            ],
            options={
                'verbose_name': 'TiltBridge',
                'verbose_name_plural': 'TiltBridges',
            },
        ),
        migrations.RemoveField(
            model_name='tiltconfiguration',
            name='average_period_secs',
        ),
        migrations.RemoveField(
            model_name='tiltconfiguration',
            name='bluetooth_device_id',
        ),
        migrations.RemoveField(
            model_name='tiltconfiguration',
            name='median_window_vals',
        ),
        migrations.AddField(
            model_name='tiltconfiguration',
            name='coefficients_up_to_date',
            field=models.BooleanField(default=True, help_text='Have the calibration points changed since the coefficient calculator was run?'),
        ),
        migrations.AddField(
            model_name='tiltconfiguration',
            name='connection_type',
            field=models.CharField(choices=[('Bluetooth', 'Bluetooth'), ('Bridge', 'TiltBridge')], default='Bluetooth', help_text='How should Fermentrack connect to this Tilt?', max_length=32),
        ),
        migrations.AddField(
            model_name='tiltconfiguration',
            name='grav_constant_term',
            field=models.FloatField(default=0.0, help_text='The constant term in the gravity calibration equation'),
        ),
        migrations.AddField(
            model_name='tiltconfiguration',
            name='grav_first_degree_coefficient',
            field=models.FloatField(default=1.0, help_text='The first degree coefficient in the gravity calibration equation'),
        ),
        migrations.AddField(
            model_name='tiltconfiguration',
            name='grav_second_degree_coefficient',
            field=models.FloatField(default=0.0, help_text='The second degree coefficient in the gravity calibration equation'),
        ),
        migrations.AddField(
            model_name='tiltconfiguration',
            name='smoothing_window_vals',
            field=models.IntegerField(default=70, help_text='Number of readings to include in the smoothing window.'),
        ),
        migrations.AlterField(
            model_name='tiltconfiguration',
            name='polling_frequency',
            field=models.IntegerField(default=15, help_text='How frequently Fermentrack should update the temp/gravity reading'),
        ),
        migrations.AddField(
            model_name='tiltconfiguration',
            name='tiltbridge',
            field=models.ForeignKey(blank=True, default=None, help_text='TiltBridge device to use (if any)', null=True, on_delete=django.db.models.deletion.SET_NULL, to='gravity.TiltBridge'),
        ),
        migrations.AlterField(
            model_name='gravitysensor',
            name='active_log',
            field=models.ForeignKey(blank=True, default=None, help_text='The currently active log of readings', null=True, on_delete=django.db.models.deletion.SET_NULL, to='gravity.GravityLog'),
        ),
    ]
