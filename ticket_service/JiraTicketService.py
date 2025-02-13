from .TicketService import TicketService
import logging


class JiraTicketService(TicketService):
    def __init__(self, config):
        self.config = config

    def create_ticket(self, data):
        logging.info("creating ticket:{}".format(data))
