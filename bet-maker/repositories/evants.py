from models.events import Event
from repositories.base import ItemRepositoryAbstract


class EventRepository(ItemRepositoryAbstract[Event]):
    model = Event
