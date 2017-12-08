# Generated by Django 2.0 on 2017-12-08 16:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bean',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('price', models.DecimalField(decimal_places=3, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Coffee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('espresso_shots', models.PositiveIntegerField(default=1)),
                ('water', models.FloatField()),
                ('steamed_milk', models.BooleanField(default=False)),
                ('foam', models.FloatField()),
                ('extra_instructions', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=3, max_digits=6, null=True)),
                ('bean', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='beans.Bean')),
            ],
        ),
        migrations.CreateModel(
            name='Powder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=3, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Roast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=3, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Syrup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=3, max_digits=5)),
            ],
        ),
        migrations.AddField(
            model_name='coffee',
            name='powders',
            field=models.ManyToManyField(blank=True, to='beans.Powder'),
        ),
        migrations.AddField(
            model_name='coffee',
            name='roast',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='beans.Roast'),
        ),
        migrations.AddField(
            model_name='coffee',
            name='syrups',
            field=models.ManyToManyField(blank=True, to='beans.Syrup'),
        ),
        migrations.AddField(
            model_name='coffee',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
