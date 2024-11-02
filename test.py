from src.utils.alert_handling import load_csv, create_alerts_from_dataframe
from src.models.session_manager import session_manager

df = load_csv("C:/Users/jacoes/Downloads/SCAPIS2Spectrum_Alerts_2024-11-01.csv")
all_alerts = create_alerts_from_dataframe(df, session_manager.project_instance)
print(all_alerts)