class Alert:
    def __init__(self, title: str, alert_dict: dict, active: bool):
        """
        Initialize an Alert instance.

        :param title: The title of the alert.
        :param alert_dict: A dictionary containing the alert details.
        :param active: TRUE or FALSE.
        """
        self.title = title
        self.alert_dict = alert_dict
        self.active = active

    def __str__(self):
        return (f"Alert Title: {self.title}\n"
                f"Alert Details: {self.alert_dict}\n"
                f"Active: {self.active}")

    def get_dict(self):
        """
        Returns the condition for this alert in a human-readable form.
        """
        return self.alert_dict

    def is_active(self):
        """
        Checks if the alert is active.
        """
        return self.active
    
class AlertManager:
    def __init__(self):
        self.alerts = []

    def add_alert(self, alert: Alert):
        self.alerts.append(alert)

    def get_alerts_by_variable(self, variable: str):
        """
        Retrieve all alerts containing the specified variable.
        """
        return [alert for alert in self.alerts if variable in alert.alert_dict.get("variables", [])]

    def get_alerts_by_title(self, title: str):
        """
        Retrieve all alerts with the specified title.
        """
        return [alert for alert in self.alerts if alert.title == title]