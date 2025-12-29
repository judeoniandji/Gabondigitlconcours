from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('concours', '0003_add_reference_to_dossier'),
    ]

    operations = [
        migrations.AddField(
            model_name='concours',
            name='publie',
            field=models.BooleanField(),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Serie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('concours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='series', to='concours.concours')),
            ],
        ),
        migrations.CreateModel(
            name='Matiere',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('coefficient', models.DecimalField(decimal_places=2, max_digits=5)),
                ('serie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matieres', to='concours.serie')),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valeur', models.DecimalField(decimal_places=2, max_digits=5)),
                ('etat', models.CharField(choices=[('brouillon', 'Brouillon'), ('valide', 'Valide')], default='brouillon', max_length=10)),
                ('date_saisie', models.DateTimeField(auto_now_add=True)),
                ('date_validation', models.DateTimeField(blank=True, null=True)),
                ('candidat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.candidat')),
                ('matiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='concours.matiere')),
                ('saisi_par', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notes_saisies', to='users.user')),
                ('valide_par', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notes_validees', to='users.user')),
            ],
        ),
    ]