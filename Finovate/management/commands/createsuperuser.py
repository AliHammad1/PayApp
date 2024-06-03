from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError

class Command(createsuperuser.Command):
    def handle(self, *args, **options):
        options.setdefault('interactive', False)
        database = options.get('database')
        user_data = {
            'username': options['username'],
            'password': options['password'],
            'email': options['email'],
            'is_verified': True  # Default to True or based on your requirements
        }
        user = self.UserModel._default_manager.db_manager(database).create_superuser(**user_data)
        if options.get('verbosity', 0) >= 1:
            self.stdout.write("Superuser created successfully.")
