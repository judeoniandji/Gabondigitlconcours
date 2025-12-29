from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concours', '0002_dossier_resultat'),
    ]

    operations = [
        migrations.AddField(
            model_name='dossier',
            name='reference',
            field=models.CharField(max_length=100, unique=True, null=True, blank=True),
        ),
    ]