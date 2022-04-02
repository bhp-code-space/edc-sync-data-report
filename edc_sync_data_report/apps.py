
from datetime import datetime
from dateutil.tz import gettz
from django.apps import AppConfig as DjangoAppConfig

from edc_base.apps import AppConfig as BaseEdcBaseAppConfig
from edc_protocol.apps import AppConfig as BaseEdcProtocolAppConfig


class AppConfig(DjangoAppConfig):
    name = 'edc_sync_data_report'



class EdcBaseAppConfig(BaseEdcBaseAppConfig):
    project_name = 'EDC SYNC Data Report'
    institution = 'Botswana-Harvard AIDS Institute'


class EdcProtocolAppConfig(BaseEdcProtocolAppConfig):
    protocol = 'BHP999'
    protocol_name = 'EDC SYNC Data Report'
    protocol_number = '999'
    protocol_title = ''
    study_open_datetime = datetime(
        2020, 7, 1, 0, 0, 0, tzinfo=gettz('UTC'))
    study_close_datetime = datetime(
        2025, 6, 30, 23, 59, 59, tzinfo=gettz('UTC'))
