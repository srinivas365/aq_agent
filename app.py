from notify_service import SlackNotifier
from ticket_service import JiraTicketService
from dotenv import  load_dotenv
import os

if __name__ == '__main__':
    load_dotenv()
    slack_config = {
        "webhook_url": os.getenv("SLACK_WEBHOOK_URL")
    }
    notifier = SlackNotifier(slack_config)
    notifier.send_notification({ "text": "hello world from aq_agent"})

    jira_config = {}
    ticket = {}
    tkt_service = JiraTicketService(jira_config)
    tkt_service.create_ticket(ticket)

