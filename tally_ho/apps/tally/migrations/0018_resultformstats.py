# Generated by Django 2.1.1 on 2020-02-12 13:12

from django.db import migrations, models
import django.db.models.deletion
import enumfields.fields
import tally_ho.libs.models.enums.form_state


class Migration(migrations.Migration):

    dependencies = [
        ('tally', '0017_auto_20190214_0849'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultFormStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('form_state', enumfields.fields.EnumIntegerField(enum=tally_ho.libs.models.enums.form_state.FormState)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('result_form', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tally.ResultForm')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tally.UserProfile')),
            ],
        ),
    ]