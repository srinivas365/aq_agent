from .TicketService import TicketService
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
class JiraTicketService(TicketService):
    def __init__(self, config):
        self.config = config

    def create_ticket(self, data):
        logging.info("creating ticket:{}".format(data))
