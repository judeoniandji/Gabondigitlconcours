from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_merge_0005_add_token_valid_after_0005_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('candidat', 'Candidat'), ('gestionnaire', 'Gestionnaire'), ('jury', 'Jury'), ('secretaire', 'Secrétaire'), ('correcteur', 'Correcteur'), ('president_jury', 'Président de jury')], max_length=20),
        ),
        migrations.AddField(
            model_name='candidat',
            name='nom_complet',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='candidat',
            name='ville_naissance',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='candidat',
            name='numero_candidat',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]