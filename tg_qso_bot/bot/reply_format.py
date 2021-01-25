from tg_qso_bot.models import Qso


def format_qso(q: Qso) -> str:
    return f"{q.call_sign_2:<6} {q.date.strftime('%d.%m.%y'):<8} {q.band:<3} {q.mode}"
