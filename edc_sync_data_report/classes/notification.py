import os
from datetime import date, datetime, timedelta
from smtplib import SMTPAuthenticationError, SMTPException

import pandas as pd
import requests
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from edc_sync_data_report.classes import ReportSummaryData
from edc_sync_data_report.classes.does_transaction_exists_in_central_server import \
    DoesTransactionExistsInCentralServer
from edc_sync_data_report.classes.server_collect_summary_data import \
    ServerCollectSummaryData
from edc_sync_data_report.models import SyncSite


# TODO test the following class


class Notification:
    """ Build a summary report for each active sync site then send a report to an email.
    """

    def __init__(self, active_sites=None):
        self.sites = active_sites or SyncSite.objects.filter(valid_to__gte=date.today())

    def build_all_sites_report(self):
        sites_summary_report = []
        for site in self.sites:
            data = []
            URL = f"http://{site.server}/api/live_data/"
            try:
                response = requests.get(URL, timeout=45)
                client_data = response.json()
                tmp = []
                server_report = ServerCollectSummaryData()
                server_data = server_report.build_summary(site_id=site.site_id)
                report = ReportSummaryData(server_data=server_data,
                                           client_data=client_data)
                matching, not_matching = report.data_comparison()
                site_report = {f"{site.name}_{site.site_id}": not_matching}
                tmp.append(site_report)

                # Build detailed report
                sync_transaction_date = date.today() - timedelta(days=1)
                created_date = datetime.strptime(
                    sync_transaction_date, '%Y-%m-%d')
                url = (f"http://{site.server}/edc_sync_data_report/api/{site.site_id}/"
                       f"{created_date}/confirmation_data/")
                response = requests.get(url, timeout=45)
                data = response.json()
                run_validation = DoesTransactionExistsInCentralServer()
                missing_records = run_validation.sync_data_check(data=data)
                detailed_data = [[r.record.get("model_name"), r.record.get("primary_key")]
                                 for r in missing_records]
                sync_detailed_df = pd.DataFrame(data=detailed_data,
                                                columns=['ModelName',
                                                         'Primary '
                                                         'Key/Transaction ID'])
                filename = (f'Sync Report-{site.name}({site.site_id})-'
                            f'{sync_transaction_date}.csv')
                detailed_report_file_path = os.path.join(settings.SYNC_REPORTS, filename)
                sync_detailed_df.to_csv(detailed_report_file_path, index=False, sep=',',
                                        encoding='utf-8')
                tmp.append(detailed_report_file_path)
                sites_summary_report.append(tmp)

            except requests.exceptions.Timeout:
                pass
            except Exception as ex:
                print(ex)
        return sites_summary_report

    def build(self):
        print("preparing sync report.")
        _data = self.build_all_sites_report()
        if len(_data) == 0:
            self.send(subject="EDC Synchronization Report",
                      template_body_name="message_noreport.html")
        else:
            for data in _data:
                summary, file_path = data
                name = None
                report = None
                for key in summary:
                    name, _ = key.split('_')
                    report = data.get(key)
                self.send(site_name=name, report=report,
                          template_body_name="message_body.html",
                          subject="EDC Synchronization Report", report_file=file_path)
        print("Done.")

    def send(self, site_name=None, report=None, template_body_name=None, subject=None,
             report_file=None):
        try:
            merge_data = {
                'community': site_name, 'sync_report': report, "report_date": date.today()
            }
            text_body = render_to_string("message_body.txt", merge_data)
            html_body = render_to_string(template_body_name or "message_body.html",
                                         merge_data)

            msg = EmailMultiAlternatives(subject=subject,
                                         from_email=settings.EMAIL_HOST_USER,
                                         to=settings.SYNC_ADMINS, body=text_body)
            # Attach detailed report
            msg.attach_alternative(html_body, "text/html")
            with open(report_file, 'w', encoding='utf-8') as detailed_report:
                msg.attach(detailed_report.name, report_file.read(), 'text/csv')

            msg.send()
        except SMTPAuthenticationError as e1:
            print("An error occurred, ", e1)
        except SMTPException as e2:
            print("An error occurred, ", e2)
        except Exception as e3:
            print(f'Mail Sending Failed!, got an error: {e3}')
