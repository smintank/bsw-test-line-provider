from sqlalchemy.ext.asyncio import AsyncSession

from models.bets import Bet
from repositories.bets import BetRepository


class BetService:
    @staticmethod
    async def create_new_bet(db: AsyncSession, bet_data: dict) -> int:
        bet = Bet(**bet_data)
        return await BetRepository.create_bet(db, bet)
