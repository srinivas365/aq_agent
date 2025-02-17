from datetime import datetime

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

    # initialize mongodb client
    dbclient = pymongo.MongoClient(os.environ.get("MONGO_URI"))

    # initializing the slack service
    slack_config = {
        "webhook_url": os.getenv("SLACK_WEBHOOK_URL")
    }
    notifier = SlackNotifier(slack_config)

    # initializing the ticket service
    tkt_service = JiraTicketService(dbclient)

    # initializing the vectordb service
    dbservice = VectorDBService()

    # initializing the bot
    bot = GroqBot(dbclient, notifier)

    try:
        while True:
            query = input("report query[enter exit to close]:")

            if query == "":
                continue

            if query == "exit":
                break
            results = dbservice.search("articles", query, 2)
            for report in results.objects:
                print(
                    f"uuid: {report.uuid}, report: {report.properties['name']}, similarity_score: {report.metadata.distance}")

            feedback = input("Are you satified with the results[y/n]:")

            escalated_info = None

            if feedback.lower() == 'n':
                print("Starting Groq chat for further details...")
                bot.collect_report_details()
                bot.confirm_and_summarize()
                ticket_id = bot.report_id
                escalated_info = {
                    "ticket_id": ticket_id,
                    "report_details": bot.report_details["summary"],
                    "timestamp": datetime.now(),
                    "user_original_query": query,
                }

            # create ticket if escalated
            if escalated_info is not None:
                tkt_service.create_ticket(escalated_info)
                print(f"Ticket has been created with id {ticket_id}. Team will reach you shortly...")
            print('\n')

        print(f"Closing the application")
    except Exception as e:
        print("exception:", str(e))
    finally:
        dbservice.close()
        dbclient.close()


