from django.contrib.auth import get_user_model
from django.test import override_settings, TestCase

from edc_sync_data_report.classes.does_transaction_exists_in_central_server import \
    DoesTransactionExistsInCentralServer

User = get_user_model()


@override_settings(ROOT_URLCONF='myapp.urls')  # replace with your app's root urlconf
class DoesTransactionExistsInCentralServerTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='john', email='john@example.com',
                                             password='doe')
        self.utility = DoesTransactionExistsInCentralServer()

    def test_sync_data_check_with_existing_record(self):
        data = [{'model_name': 'User', 'primary_key': self.user.id, 'app_label': 'auth'}]
        result = self.utility.sync_data_check(data=data)

        # Since we are checking for missing records, and since we've just created a user,
        # the result should be an empty list
        self.assertEqual(result, [])

    def test_sync_data_check_with_non_existent_record(self):
        data = [{'model_name': 'User', 'primary_key': 999999,
                 'app_label': 'auth'}]  # Non-existent user
        result = self.utility.sync_data_check(data=data)

        # The user with id 999999 does not exist, so the result should contain our data
        # item
        self.assertEqual(result, data)
