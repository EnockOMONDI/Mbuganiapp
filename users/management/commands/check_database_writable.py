from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction


class Command(BaseCommand):
    help = 'Verify that the configured database accepts schema writes before migrations run.'

    def handle(self, *args, **options):
        vendor = connection.vendor
        table_name = '_mbugani_deploy_write_check'

        try:
            with connection.cursor() as cursor:
                if vendor == 'postgresql':
                    cursor.execute('SHOW transaction_read_only')
                    read_only = cursor.fetchone()[0]
                    cursor.execute('SELECT pg_is_in_recovery()')
                    in_recovery = cursor.fetchone()[0]
                    self.stdout.write(f'PostgreSQL transaction_read_only={read_only}, pg_is_in_recovery={in_recovery}')

                    if read_only == 'on' or in_recovery:
                        raise CommandError(
                            'The configured PostgreSQL database is read-only. '
                            'Update DATABASE_URL in Render to the primary writable Supabase connection, '
                            'then redeploy.'
                        )

                    with transaction.atomic():
                        cursor.execute(f'CREATE TABLE "{table_name}" (id integer)')
                        cursor.execute(f'DROP TABLE "{table_name}"')
                else:
                    with transaction.atomic():
                        cursor.execute(f'CREATE TABLE "{table_name}" (id integer)')
                        cursor.execute(f'DROP TABLE "{table_name}"')
        except CommandError:
            raise
        except Exception as exc:
            raise CommandError(
                'Database write check failed. Confirm the deployed DATABASE_URL points to a writable primary database '
                f'and that the database user can create tables. Original error: {exc}'
            ) from exc

        self.stdout.write(self.style.SUCCESS('Database write check passed.'))
