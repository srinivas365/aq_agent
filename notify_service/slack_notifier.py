from .notifier import Notifier
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class SlackNotifier(Notifier):
    def __init__(self, config):
        self.config = config

    def send_notification(self, payload):
        headers = {"Content-Type": "application/json"}
        try:
            logging.info("creating a notification in slack channel:{}".format(payload))
            response = requests.post(self.config['webhook_url'], json=payload, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to send Slack notification: {e}")
            return False
        return True
