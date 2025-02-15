from models.events import EventStatus

EVENT_STATUS_MAPPING = {
    1: EventStatus.NOT_FINISHED,
    2: EventStatus.WIN,
    3: EventStatus.LOSE,
}
