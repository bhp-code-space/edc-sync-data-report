

class ReportSummaryData:

    def __init__(self, server_data, client_data):
        self.server_summary_data = server_data
        self.client_data = client_data

    def data_comparison(self):
        matching = []
        not_matching = []

        server_keys = set(self.server_summary_data.keys())
        client_keys = set(self.client_data.keys())
        shared_keys = client_keys.intersection(server_keys)
        for key in shared_keys:
            server_value = self.server_summary_data.get(key)
            client_value = self.client_data.get(key)
            if server_value != client_value:
                data = {f'{key}': {'client': client_value, 'server': server_value}}
                not_matching.append(data)
            elif server_value == client_value:
                data = {f'{key}': {'client': client_value, 'server': server_value}}
                matching.append(data)
        return matching, not_matching
