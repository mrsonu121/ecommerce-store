from django.db import migrations


class Migration(migrations.Migration):

    # No direct app migration dependency; this migration only creates
    # a DB index on the built-in auth_user table.
    dependencies = []

    operations = [
        migrations.RunSQL(
            sql=(
                "CREATE INDEX IF NOT EXISTS auth_user_email_idx ON auth_user (email);"
            ),
            reverse_sql=(
                "DROP INDEX IF EXISTS auth_user_email_idx;"
            ),
        ),
    ]
