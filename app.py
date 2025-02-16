import pymongo

from notify_service import SlackNotifier
from ticket_service import JiraTicketService
from dotenv import  load_dotenv
import os
import logging
import uuid
from vectordb_service import VectorDBService
from groq_service import GroqBot

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    load_dotenv()
    logging.info("loading config from env")
    logging.info("starting app")

    # initializing the slack service
    slack_config = {
        "webhook_url": os.getenv("SLACK_WEBHOOK_URL")
    }
    notifier = SlackNotifier(slack_config)

    # initializing the ticket service
    jira_config = {}
    tkt_service = JiraTicketService(jira_config)

    # initializing the vectordb service
    dbservice = VectorDBService()

    # initialize mongodb client
    dbclient = pymongo.MongoClient(os.environ.get("MONGO_URI"))

    # initializing the bot
    bot = GroqBot(dbclient, notifier)

    while True:
        query = input("report query[enter exit to close]:")
        if query == "exit":
            break
        results = dbservice.search("articles", query, 2)
        for report in results.objects:
            print(f"uuid: {report.uuid}, report: {report.properties['name']}, similarity_score: {report.metadata.distance}")

        feedback = input("Are you satified with the results[y/n]:")
        if feedback.lower() == 'n':
            print("Starting Groq chat for further details...")
            bot.collect_report_details()
            bot.confirm_and_summarize()
            ticket_id = bot.report_id
            tkt_service.create_ticket({"ticket_id": ticket_id, "report_details": bot.report_details})
            print(f"Ticket has been created with id {ticket_id}. Team will reach you shortly...")

    print(f"Closing the application")
    dbservice.close()
    dbclient.close()

