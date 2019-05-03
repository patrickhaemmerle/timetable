from django.core.management import BaseCommand
from urllib.request import urlopen
from zipfile import ZipFile

ZIP = 'gtfs/gtfs.zip'
EXTRACTED = 'gtfs/gtfs'

class Command(BaseCommand):

    def handle(self, *args, **options):
        data = urlopen("https://opentransportdata.swiss/dataset/timetable-2019-gtfs/permalink")
        with open(ZIP, 'wb') as output:
            output.write(data.read())

        zip_ref = ZipFile(ZIP, 'r')
        zip_ref.extractall(EXTRACTED)
        zip_ref.close()
