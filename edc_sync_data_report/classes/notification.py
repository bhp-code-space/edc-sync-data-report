import requests

from datetime import date
from django.conf import settings

from edc_sync_data_report.classes import ReportSummaryData
from edc_sync_data_report.classes.server_collect_summary_data import ServerCollectSummaryData
from edc_sync_data_report.models import SyncSite, SyncAPIs

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from smtplib import SMTPException, SMTPAuthenticationError

#TODO test the following class


class Notification:

    """
        Build a summary report for each active sync site then send a report to an email.
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

                server_report = ServerCollectSummaryData()
                server_data = server_report.build_summary(site_id=site.site_id)
                report = ReportSummaryData(server_data=server_data, client_data=client_data)
                matching, not_matching = report.data_comparison()
                site_report = {f"{site.name}_{site.site_id}": not_matching}
                sites_summary_report.append(site_report)
            except requests.exceptions.Timeout:
                pass
            except Exception as ex:
                print(ex)
        return sites_summary_report

    def build(self):
        print("preparing sync report.")
        if len(self.build_all_sites_report()) == 0:
            self.send(subject="EDC Synchronization Report", template_body_name="message_noreport.html")
        else:
            for data in self.build_all_sites_report():
                name = None
                report = None
                for key in data:
                    name, _ = key.split('_')
                    report = data.get(key)
                self.send(site_name=name, report=report, template_body_name="message_body.html",
                          subject="EDC Synchronization Report")
        print("Done.")

    def send(self, site_name=None, report=None, template_body_name=None, subject=None):
        try:
            merge_data = {
                'community': site_name, 'sync_report': report, "report_date": date.today()
            }
            text_body = render_to_string("message_body.txt", merge_data)
            html_body = render_to_string(template_body_name or "message_body.html", merge_data)

            msg = EmailMultiAlternatives(subject=subject, from_email=settings.EMAIL_HOST_USER,
                                         to=settings.SYNC_ADMINS, body=text_body)
            msg.attach_alternative(html_body, "text/html")
            msg.send()
        except SMTPAuthenticationError as e1:
            print("An error occurred, ", e1)
        except SMTPException as e2:
            print("An error occurred, ", e2)
        except:
            print("Mail Sending Failed!")
