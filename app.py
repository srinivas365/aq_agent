from notify_service import SlackNotifier
from ticket_service import JiraTicketService
from dotenv import  load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    load_dotenv()
    logging.info("loading config from env")
    logging.info("starting app")
    slack_config = {
        "webhook_url": os.getenv("SLACK_WEBHOOK_URL")
    }
    notifier = SlackNotifier(slack_config)
    notifier.send_notification({ "text": "hello world from aq_agent"})

    jira_config = {}
    ticket = {}
    tkt_service = JiraTicketService(jira_config)
    tkt_service.create_ticket(ticket)

