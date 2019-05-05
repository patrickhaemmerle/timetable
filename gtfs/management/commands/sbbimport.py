import csv
import shutil
import sys

from django.core.management import BaseCommand
from urllib.request import urlopen
from zipfile import ZipFile

from django.db import transaction

from gtfs.models import Agency, Stop, Route, Transfer

ZIP = 'gtfs/gtfs.zip'
EXTRACTED = 'gtfs/gtfs'


class Command(BaseCommand):

    def handle(self, *args, **options):

        if not options['no_download']:
            self.download()

        with transaction.atomic():
            self.clear_data()
            self.import_agencies()
            self.import_stops()
            self.import_routes()
            self.import_transfers()

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-download',
            action='store_true',
            help='Only import previously downloaded data',
        )

    def download(self):
        shutil.rmtree(EXTRACTED)
        data = urlopen('https://opentransportdata.swiss/dataset/timetable-2019-gtfs/permalink')
        with open(ZIP, 'wb') as output:
            output.write(data.read())

        zip_ref = ZipFile(ZIP, 'r')
        zip_ref.extractall(EXTRACTED)
        zip_ref.close()

    def clear_data(self):
        print('Clear old data ... ', end='')
        sys.stdout.flush()

        Transfer.objects.all().delete()
        Route.objects.all().delete()
        Stop.objects.all().delete()
        Agency.objects.all().delete()
        print('done')

    def import_agencies(self):
        print('Import agencies ... ', end='')
        sys.stdout.flush()

        with open(EXTRACTED + '/agency.txt', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in csv_reader:
                Agency.objects.create(**row)
        print('done')

    def import_stops(self):
        print('Import stops ... ', end='')
        sys.stdout.flush()

        with open(EXTRACTED + '/stops.txt', newline='', encoding='utf-8-sig') as csvfile:
            csv_reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')

            for row in csv_reader:
                # Default the int fields
                if row['parent_station'] == '':
                    row['parent_station'] = None
                if row['location_type'] == '':
                    row['location_type'] = 0

                # Rename parent station to insert the id and not an object
                row['parent_station_id'] = row.pop('parent_station')

                # Get and process platform information which is in the id (in the case of SBB)
                split_id = row['stop_id'].split(':')
                if row['location_type'] == 0 and len(split_id) >= 3:
                    row['platform_code'] = split_id[2]

                Stop.objects.create(**row)

            print('done')

    def import_routes(self):
        print('Import routes ... ', end='')
        sys.stdout.flush()

        with open(EXTRACTED + '/routes.txt', newline='', encoding='utf-8-sig') as csvfile:
            csv_reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in csv_reader:
                Route.objects.create(**row)
        print('done')

    def import_transfers(self):
        print('Import transfers ... ', end='')
        sys.stdout.flush()

        with open(EXTRACTED + '/transfers.txt', newline='', encoding='utf-8-sig') as csvfile:
            csv_reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in csv_reader:
                Transfer.objects.create(**row)
        print('done')