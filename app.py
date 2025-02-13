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

    # initializing the bot
    bot = GroqBot()


    while True:
        query = input("report query[enter exit to close]:")
        if query == "exit":
            break
        results = dbservice.search("articles", query, 2)
        for report in results.objects:
            print(f"uuid: {report.uuid}, report: {report.properties['name']}, similarity_score: {report.metadata.distance}")

        feedback = input("Are you satified with the results[agent/ai]:")
        if feedback.lower() == 'ai':
            print("Starting Groq chat for further details...")
            bot.collect_report_details()
            bot.confirm_and_summarize()

        if feedback.lower() == "agent":
            print("escalating to team......")
            report_text = input("Describe your report in detail:")
            year = input("Any specific year:")
            add_info = input("Any additional info:")
            mail_id = input("your mailId:")
            ticket_id = str(uuid.uuid4())
            notification_msg = f'''
            User has queried about the report with attached information.
            ticket_id: {ticket_id}
            report: {report_text}
            year: {year}
            additional_info: {add_info}
            requested by: {mail_id}
            '''
            notifier.send_notification({"text": notification_msg})
            ticket = {
                "report_text": report_text,
                "year": year,
                "add_info": add_info,
                "mail_id": mail_id,
                "ticket_id": ticket_id,
            }
            tkt_service.create_ticket(ticket)
            print(f"ticket has been created with id {ticket_id}. Team will reach you shortly...")

    print(f"Closing the application")
    dbservice.close()

