import pytest

from constants import EVENT_STATUS_MAPPING
from models.events import EventStatus


@pytest.mark.parametrize(
    "code, status", [(k, v) for k, v in EVENT_STATUS_MAPPING.items()]
)
def test_event_correct_status_mapping(code: int, status: EventStatus) -> None:
    assert EVENT_STATUS_MAPPING[code] == status


@pytest.mark.parametrize("code", [0, 4, -1])
def test_event_wrong_status_mapping(code: int) -> None:
    with pytest.raises(KeyError) as error:
        assert EVENT_STATUS_MAPPING[code] == error
