import pytest
from datetime import datetime, timedelta
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager
from main import app
from database import events

@pytest.fixture
async def client():
    async with LifespanManager(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url='http://localhost') as ac:
            yield ac

@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_simple_workflow(client, anyio_backend):
    events.clear()
    test_id = 4
    event_data = {
        'deadline': (datetime.now() + timedelta(minutes=1)).isoformat(),
        'coefficient': 1.2
    }
    created_event = event_data | {'state': 1, 'event_id': test_id}


    create_response = await client.post('/events/', json=event_data)
    assert create_response.status_code == 201


    get_response = await client.get(f'/events/{test_id}/')
    assert get_response.status_code == 200
    assert get_response.json() == created_event


    updated_event = created_event.copy()
    updated_event['state'] = 2
    update_response = await client.patch(f'/events/{test_id}/', json=updated_event)
    assert update_response.status_code == 200
    assert update_response.json() == updated_event


    list_response = await client.get('/events/')
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1 