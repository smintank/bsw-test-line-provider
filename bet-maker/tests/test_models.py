from models.bets import EventStatus


def test_bet_status_enum():

    assert EventStatus.NOT_FINISHED.value == "not_finished"
    assert EventStatus.WIN.value == "win"
    assert EventStatus.LOSE.value == "lose"