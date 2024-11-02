from src.redcap import Project
from src.models.alert import Alert

class redcapProj(Project):
    def __init__(self, api_url, api_token):
        super().__init__(api_url, api_token)
        self.alerts = []

    def add_alert(self, title, alert_dict, active):
        alert = Alert(title, alert_dict, active)
        self.alerts.append(alert)

    def evaluate_alerts(self, data_row):
        triggered_alerts = []
        for alert in self.alerts:
            if alert.is_triggered(data_row):
                triggered_alerts.append(alert)
        return triggered_alerts
    
    def show_alerts(self):
        for alert in self.alerts:
            print(alert)