from django.core.management import BaseCommand

#The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
    # Show this when the user types help
    help = "runs 101worker"

    # A command must define handle()
    def handle(self, *args, **options):
        self.stdout.write("Doing All The Things!")
