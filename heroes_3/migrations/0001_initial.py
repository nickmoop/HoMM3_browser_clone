# Generated by Django 2.0.7 on 2018-11-12 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Battles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('state', models.CharField(max_length=10)),
                ('creator_castle', models.CharField(max_length=20)),
                ('guest_castle', models.CharField(max_length=20, null=True)),
                ('growth', models.IntegerField()),
                ('log', models.CharField(max_length=20000, null=True)),
                ('_units', models.CharField(max_length=20000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Players',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nick_name', models.CharField(max_length=40)),
                ('rating', models.FloatField(default=1000)),
                ('win_count', models.IntegerField(default=0)),
                ('loose_count', models.IntegerField(default=0)),
                ('level', models.IntegerField(default=0)),
                ('experience', models.IntegerField(default=0)),
                ('special', models.CharField(max_length=255, null=True)),
                ('spells_names', models.CharField(max_length=1000, null=True)),
                ('battle_spells', models.CharField(max_length=1000, null=True)),
                ('spell_to_cast', models.CharField(max_length=100, null=True)),
                ('current_mp', models.IntegerField(default=0)),
                ('_skills', models.CharField(max_length=255, null=True)),
                ('_attributes', models.CharField(default='{"Attack": 0, "Defence": 0, "Spell Power": 0, "Knowledge": 0}', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=40)),
                ('email', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=40)),
                ('token', models.CharField(max_length=80, null=True)),
                ('battle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='heroes_3.Battles')),
                ('player', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='heroes_3.Players')),
            ],
        ),
        migrations.AddField(
            model_name='battles',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creator', to='heroes_3.Players'),
        ),
        migrations.AddField(
            model_name='battles',
            name='guest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='guest', to='heroes_3.Players'),
        ),
    ]