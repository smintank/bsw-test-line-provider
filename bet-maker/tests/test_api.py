import httpx
import pytest
import pytest_asyncio
import respx

from models.bets import EventStatus
from services.event_services import LineProviderService



@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_bet_workflow(client: httpx.AsyncClient, anyio_backend, mock_external_api, mock_http_client):

    bet_data = {
        "event_id": 1,
        "amount": 10.0
    }

    create_response = await mock_http_client.post('/bet/', json=bet_data)
    assert create_response.status_code == 201
    created_bet = create_response.json()
    assert "bet_id" in created_bet

    get_bets_response = await client.get('/bets/')
    assert get_bets_response.status_code == 200
    bets = get_bets_response.json()
    assert len(bets) > 0

    bet_from_list = bets[0]
    assert bet_from_list["amount"] == 10.0
    assert bet_from_list["event_id"] == 1
    assert bet_from_list["status"] == EventStatus.NOT_FINISHED.name