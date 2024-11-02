class SessionManager:
    def __init__(self):
        self.api_token = None
        self.project_instance = None

    def set_api_token(self, api_token):
        self.api_token = api_token

    def get_api_token(self):
        return self.api_token

    def set_project_instance(self, project_instance):
        self.project_instance = project_instance

    def get_project_instance(self):
        return self.project_instance

# Create a global session manager instance
session_manager = SessionManager()