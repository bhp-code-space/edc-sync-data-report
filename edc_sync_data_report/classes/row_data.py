

class RowData:

    def __init__(self, model_name, server_value, client_value, label=None):
        self.model_name = model_name
        self.server_value = server_value
        self.client_value = client_value
        self.label = label

    @property
    def diff(self):
        if self.server_value > self.client_value:
            return self.server_value - self.client_value
        else:
            return self.client_value - self.server_value

    def matching_label(self):
        return self.label