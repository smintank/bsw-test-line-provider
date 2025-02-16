import pytest

from models.events import EventStatus


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_bet_workflow(anyio_backend, mock_http_client):
    bet_data = {"event_id": 1, "amount": 10.0}

    # Отправляем запрос на создание ставки
    create_response = await mock_http_client.post("/bet/", json=bet_data)
    assert create_response.status_code == 201

    created_bet = create_response.json()
    assert "id" in created_bet and isinstance(created_bet["id"], int)

    # Получаем список ставок
    get_bets_response = await mock_http_client.get("/bets/")
    assert get_bets_response.status_code == 200

    bets = get_bets_response.json()
    assert len(bets) > 0

    bet_from_list = bets[0]

    assert bet_from_list["amount"] == 10.0
    assert bet_from_list["event"]["event_id"] == 1
    assert bet_from_list["event"]["status"] == EventStatus.NOT_FINISHED.value
