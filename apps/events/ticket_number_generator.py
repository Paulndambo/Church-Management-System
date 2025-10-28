from datetime import datetime
from apps.events.models import ChurchEvent, ChurchEventTicketType

date_today = datetime.now().date()

def generate_ticket_number(event: ChurchEvent, ticket_type: ChurchEventTicketType, last_ticket_id: int) -> str:
    ticket_number = f"TN-{event.name[0]}/{ticket_type.title[0]}/{last_ticket_id+1}/{date_today.year}"
    return ticket_number