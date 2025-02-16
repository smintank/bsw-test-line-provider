import pytest
from aioresponses import aioresponses

from services.line_provider_api_service import LineProviderAPIService


@pytest.mark.asyncio
async def test_get_url_data_success():
    with aioresponses() as mocked_responses:
        mocked_responses.get(
            "http://line-provider:8000/events/1/",
            status=200,
            payload='{"event_id": 1, "coefficient": 1.5}',
        )

        response = await LineProviderAPIService.get_url_data(
            "http://line-provider:8000/events/1/"
        )
        assert response == {"event_id": 1, "coefficient": 1.5}
