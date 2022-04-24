from edc_sync_data_report.classes.row_data import RowData


class ReportSummaryData:

    def __init__(self, server_data, client_data):
        self.server_summary_data = server_data
        self.client_data = client_data

    def data_comparison(self):
        # TODO refactor for performance reasons
        matching = []
        not_matching = []

        server_keys = set(self.server_summary_data.keys())
        client_keys = set(self.client_data.keys())
        shared_keys = client_keys.intersection(server_keys)
        for key in shared_keys:
            server_value = self.server_summary_data.get(key)
            client_value = self.client_data.get(key)
            if server_value != client_value:
                row_data = RowData(model_name=key, server_value=server_value, client_value=client_value,
                                   label="Not matching")
                not_matching.append(row_data)
            elif server_value == client_value:
                row_data = RowData(model_name=key, server_value=server_value, client_value=client_value,
                                   label="Matching")
                matching.append(row_data)
        return matching, not_matching

    def is_all_models_matching(self):
        matching, not_matching = self.data_comparison()
        return len(not_matching) == 0
