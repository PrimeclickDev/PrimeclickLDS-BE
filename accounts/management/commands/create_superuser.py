from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create a superuser with hardcoded details.'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # Hardcoded superuser details
        email = 'ikhidea4@gmail.com'
        password = 'payboi10'
        first_name = 'Admin'
        last_name = 'User'

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR(f"Superuser with email {email} already exists."))
        else:
            superuser = User.objects.create_superuser(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            superuser.is_active = True
            superuser.save()
            self.stdout.write(self.style.SUCCESS(f"Superuser {email} created successfully."))
