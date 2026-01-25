from django.core.management.base import BaseCommand
from citas.models import Cita

class Command(BaseCommand):
    help = 'Deletes all orphaned citations (no consultorio) and clears the board state'

    def handle(self, *args, **kwargs):
        # 1. Borrar todas las citas inconsistentes (sin consultorio)
        orphans = Cita.objects.filter(consultorio__isnull=True)
        count = orphans.count()
        orphans.delete()
        
        self.stdout.write(self.style.WARNING(f'Deleted {count} orphaned citations.'))
        
        # 2. Opcional: Limpiar todas las citas para empezar de cero si el usuario lo necesita
        # Cita.objects.all().delete()
        # self.stdout.write(self.style.SUCCESS('Cleared ALL citations.'))
        
        self.stdout.write(self.style.SUCCESS('Purge complete. Database is now clean of ghosts.'))
