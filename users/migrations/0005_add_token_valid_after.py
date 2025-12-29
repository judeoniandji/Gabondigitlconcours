from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_add_jury_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='token_valid_after',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]