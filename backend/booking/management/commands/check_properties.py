from django.core.management.base import BaseCommand
from booking.models import Property

class Command(BaseCommand):
    help = 'Check if there are any properties in the database'

    def handle(self, *args, **options):
        property_count = Property.objects.count()
        self.stdout.write(f'Number of properties in database: {property_count}')
        
        if property_count > 0:
            properties = Property.objects.all()
            self.stdout.write('\nProperty details:')
            for prop in properties:
                self.stdout.write(f'\n- {prop.title} (ID: {prop.id})')
                self.stdout.write(f'  Host: {prop.host.username}')
                self.stdout.write(f'  Available: {prop.is_available}')
                self.stdout.write(f'  City: {prop.city}')
                self.stdout.write(f'  Price: ${prop.price_per_night}/night')
