from django.core.management.base import BaseCommand
from blueterra.utils import clean_trash

class Command(BaseCommand):
    help = "Clean up R2 trash files pending deletion"
    
    def handle(self, *args, **kwargs):
        clean_trash()
        # self.stdout.write(self.style.SUCCESS("R2 trash cleaned successfully"))