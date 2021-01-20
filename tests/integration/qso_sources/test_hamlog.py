from tg_qso_bot.qso_sources import hamlog


def test__session__retrieve_token__returns_csrf():
    session = hamlog._HamlogSession()
    token = session.retrieve_token()
    assert len(token) > 0


def test__qso_source__get_qso_list__count_equal_10():
    source = hamlog.HamlogQsoSource()
    qsos = source.get_qso_list("RAEM", 10)
    assert len(qsos) == 10
