import csv
import os
import shutil
import sys
from datetime import date, time, datetime

from django.core.management import BaseCommand
from urllib.request import urlopen
from zipfile import ZipFile

from django.db import transaction

from gtfs.models import Agency, Stop, Route, Transfer, Calendar, CalendarDate, Trip, StopTime

ZIP = 'gtfs/gtfs.zip'
EXTRACTED = 'gtfs/gtfs'


class Command(BaseCommand):

    def handle(self, *args, **options):

        if not options['no_download']:
            self.download()

        self.clear_data()

        with transaction.atomic():
            self.import_stops()
            self.import_agencies()
            self.import_routes()
            self.import_transfers()
            self.import_calendar()

        self.import_calendar_dates()
        self.import_trips()
        self.import_stop_times()

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-download',
            action='store_true',
            help='Only import previously downloaded data',
        )

    def download(self):
        print('Download data ... ', end='')
        sys.stdout.flush()
        if os.path.isdir(EXTRACTED):
            shutil.rmtree(EXTRACTED)
        data = urlopen('https://opentransportdata.swiss/dataset/timetable-2019-gtfs/permalink')
        with open(ZIP, 'wb') as output:
            output.write(data.read())

        zip_ref = ZipFile(ZIP, 'r')
        zip_ref.extractall(EXTRACTED)
        zip_ref.close()
        print('done')

    def clear_data(self):
        print('Clear old data ... ', end='')
        sys.stdout.flush()

        StopTime.objects.all().delete()
        Trip.objects.all().delete()
        CalendarDate.objects.all().delete()
        Calendar.objects.all().delete()
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

    def import_calendar(self):
        print('Import calendar ... ', end='')
        sys.stdout.flush()

        with open(EXTRACTED + '/calendar.txt', newline='', encoding='utf-8-sig') as csvfile:
            csv_reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in csv_reader:
                row['start_date'] = datetime.strptime(row['start_date'], '%Y%m%d')
                row['end_date'] = datetime.strptime(row['end_date'], '%Y%m%d')
                Calendar.objects.create(**row)
        print('done')

    def import_calendar_dates(self):
        print('Import calendar_dates ... ', end='')
        sys.stdout.flush()

        count = 0
        with open(EXTRACTED + '/calendar_dates.txt', newline='', encoding='utf-8-sig') as csvfile:
            csv_reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            calendar_dates = list()
            for row in csv_reader:
                row['date'] = datetime.strptime(row['date'], '%Y%m%d')
                calendar_dates.append(CalendarDate(**row))
                count += 1
                if count % 1000 == 0:
                    print('\rImport calendar_dates ... ' + 'read ' + str(count) + ' records', end='')
                    sys.stdout.flush()

            print('\rImport calendar_dates ... ' + 'inserting ' + str(count) + ' records into db', end='')
            sys.stdout.flush()
            CalendarDate.objects.bulk_create(calendar_dates)

        print('\rImport calendar_dates ... done                                       ')

    def import_trips(self):
        print('Import trips ... ', end='')
        sys.stdout.flush()

        count = 0
        with open(EXTRACTED + '/trips.txt', newline='', encoding='utf-8-sig') as csvfile:
            csv_reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            trips = list()
            for row in csv_reader:
                trips.append(Trip(**row))
                count += 1
                if count % 1000 == 0:
                    print('\rImport trips ... ' + 'read ' + str(count) + ' records', end='')
                    sys.stdout.flush()

            print('\rImport trips ... ' + 'inserting ' + str(count) + ' records into db', end='')
            sys.stdout.flush()
            Trip.objects.bulk_create(trips)

        print('\rImport trips ... done                                       ')

    def import_stop_times(self):
        print('Import stop_times ... ', end='')
        sys.stdout.flush()

        count = 0
        with open(EXTRACTED + '/stop_times.txt', newline='', encoding='utf-8-sig') as csvfile:
            csv_reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            stop_times = list()
            for row in csv_reader:
                stop_times.append(StopTime(**row))
                count += 1
                if count % 1000 == 0:
                    print('\rImport stop_times ... ' + str(count) + ' records', end='')
                    sys.stdout.flush()
                if count % 100000 == 0:
                    StopTime.objects.bulk_create(stop_times)
                    stop_times.clear()

            sys.stdout.flush()
            StopTime.objects.bulk_create(stop_times)

        print('\rImport stop_times ... done                                       ')