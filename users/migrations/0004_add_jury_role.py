from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_email'),
    ]

    operations = [
        # No schema changes required for choices update; keeping migration for tracking.
    ]