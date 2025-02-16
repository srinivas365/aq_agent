from .TicketService import TicketService
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
class JiraTicketService(TicketService):
    def __init__(self, dbclient):
        self.dbclient = dbclient
        self.db = self.dbclient[os.environ.get("MONGO_DB")]
        self.collection = self.db[os.environ.get("TICKET_COLLECTION")]

    def create_ticket(self, data):
        logging.info("creating ticket:{}".format(data))
        self.collection.insert_one(data)
