from mailwizz.client import Client as MailWizzApiClient
import os

class MailwizzAPI:
    def __init__(self):
        config = {
            'api_url': os.environ.get('MAILWIZZ_API_URL', 'https://your-mailwizz-domain.com/api'),
            'public_key': os.environ.get('MAILWIZZ_PUBLIC_KEY'),
            'secret_key': os.environ.get('MAILWIZZ_PRIVATE_KEY'),
        }
        self.client = MailWizzApiClient(config)

    def test_connection(self):
        try:
            # We'll try to get the lists as a connection test
            response = self.client.lists.get_lists(page=1, per_page=1)
            if response['status'] == 'success':
                return True, "Connection successful"
            else:
                return False, f"Connection failed with status: {response['status']}"
        except Exception as e:
            return False, f"Connection failed with error: {str(e)}"

    def get_lists(self, page=1, per_page=10):
        return self.client.lists.get_lists(page=page, per_page=per_page)

    def add_subscriber(self, list_uid, email, data=None):
        if data is None:
            data = {}
        data['EMAIL'] = email
        return self.client.subscribers.create(list_uid, data)

    def send_campaign(self, campaign_uid):
        return self.client.campaigns.update(campaign_uid, {'status': 'sending'})

# Example usage:
# api = MailwizzAPI()
# connection_status, message = api.test_connection()
# print(f"Connection status: {connection_status}")
# print(f"Message: {message}")
