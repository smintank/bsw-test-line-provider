import json

import pytest
from aioresponses import aioresponses
from httpx import RequestError

from services.event_services import LineProviderAPIService

TEST_URL = "http://line-provider:8000/events/1/"


@pytest.mark.asyncio
async def test_get_url_data_success():

    with aioresponses() as mocked_responses:
        mocked_responses.get(
            TEST_URL,
            status=200,
            payload={"event_id": 1, "coefficient": 1.5},
            repeat=True,
        )

        response = await LineProviderAPIService.get_url_data(TEST_URL)

        assert response == {"event_id": 1, "coefficient": 1.5}


@pytest.mark.asyncio
async def test_get_url_data_http_error():
    with aioresponses() as mocked_responses:
        mocked_responses.get(TEST_URL, status=404)

        response = await LineProviderAPIService.get_url_data(TEST_URL)

        assert response == {}


@pytest.mark.asyncio
async def test_get_url_data_network_error():
    with aioresponses() as mocked_responses:
        mocked_responses.get(TEST_URL, exception=RequestError("Network error"))

        response = await LineProviderAPIService.get_url_data(TEST_URL)

        assert response == {}


@pytest.mark.asyncio
async def test_get_url_data_invalid_json():
    with aioresponses() as mocked_responses:
        mocked_responses.get(
            TEST_URL, body="INVALID_JSON", headers={"Content-Type": "application/json"}
        )

        response = await LineProviderAPIService.get_url_data(TEST_URL)

        assert response == {}


@pytest.mark.asyncio
async def test_get_url_data_not_json_response():
    with aioresponses() as mocked_responses:
        mocked_responses.get(
            TEST_URL,
            body=json.dumps({"event_id": 1}),
            headers={"Content-Type": "text/html"},
        )

        response = await LineProviderAPIService.get_url_data(TEST_URL)

        assert response == {}
