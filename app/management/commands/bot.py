import schedule
from django.core.management import BaseCommand

from app.views import selenium_parser, samsara_parser, timezone

schedule.every().day.at("08:00", tz=timezone).do(selenium_parser)
schedule.every(2).hours.do(samsara_parser)


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('[+] Started Working')
        while True:
            schedule.run_pending()
