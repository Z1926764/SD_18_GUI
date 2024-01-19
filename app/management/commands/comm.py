from django.core.management.base import BaseCommand, CommandError
#from app.models import PressurePoint
#import schedule

class Command(BaseCommand):
    help = 'Does some magical work'

    def handle(self, *args, **options):
        """ Do your work here """
        #self.stdout.write('There are {} things!'.format(PressurePoint.objects.count()))
        #schedule.every(10).seconds.do(self.stdout.write('hey'))