from abc import ABC, abstractmethod


class TicketService(ABC):
    @abstractmethod
    def create_ticket(self, data):
        pass
