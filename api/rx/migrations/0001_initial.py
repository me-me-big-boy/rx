# Generated by Django 5.0.6 on 2024-05-13 21:12

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'categories',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'deliveries',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True)),
                ('names', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), size=None)),
                ('categories', models.ManyToManyField(related_name='agents', to='rx.category')),
            ],
            options={
                'ordering': ('names',),
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=8)),
                ('mu', models.CharField(choices=[('?', '?'), ('unit', 'unit'), ('wv', '% w/v'), ('ww', '% w/w'), ('mcg', 'μg'), ('mg', 'mg'), ('g', 'g'), ('ml', 'ml'), ('l', 'l')], default='?', verbose_name='measurement unit')),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rx.agent')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True)),
                ('name', models.CharField(max_length=255)),
                ('mu', models.CharField(choices=[('?', '?'), ('unit', 'unit'), ('wv', '% w/v'), ('ww', '% w/w'), ('mcg', 'μg'), ('mg', 'mg'), ('g', 'g'), ('ml', 'ml'), ('l', 'l')], default='?', verbose_name='measurement unit')),
                ('agents', models.ManyToManyField(through='rx.Ingredient', to='rx.agent')),
                ('delivery', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rx.delivery')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='ingredient',
            name='medicine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rx.medicine'),
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True)),
                ('expires_on', models.DateField()),
                ('is_discarded', models.BooleanField(default=False)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('currency', models.CharField(blank=True, max_length=3, null=True)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='available quantity')),
                ('init_quantity', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='initial quantity')),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rx.medicine')),
            ],
            options={
                'ordering': ('medicine__name',)
            },
        ),
    ]
