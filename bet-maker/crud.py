from schemas import SCreateBet, SBet, SEvent, EventState


async def create_bet(bet: SCreateBet) -> int:
    return bet.event_id


async def get_all_bets() -> list[SBet] | None:
    return [SBet(bet_id=1, amount=2.3, status=2), SBet(bet_id=2, amount=3.33, status=1)]


async def fetch_all_events() -> list[SEvent] | None:
    return [SEvent(event_id=1, status=EventState.FINISHED_WIN, coefficient=1.43, deadline=234234234234),
            SEvent(event_id=1, status=EventState.FINISHED_LOSE, coefficient=1.43, deadline=234234234234)]
