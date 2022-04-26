from datetime import date

from django.conf import settings

from edc_sync_data_report.classes import ClientCollectSummaryData
from edc_sync_data_report.classes.notification import Notification
from edc_sync_data_report.classes.summary_data import SummaryData


def send_sync_report():
    sender = Notification()
    sender.build()
    print("Testing cluster")


def prepare_confirmation_ids():
    collector = SummaryData()
    created_date = date.today()
    site_id = settings.SITE_ID
    collector.collect_primary_key_and_save(site_id=site_id, created_date=created_date)


def prepare_summary_count_data():
    collector = ClientCollectSummaryData()
    collector.create_summary_data()

