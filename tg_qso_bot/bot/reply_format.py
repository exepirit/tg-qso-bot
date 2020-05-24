from tg_qso_bot.models import Qso


def format_qso(q: Qso) -> str:
    return f"{q.call_sign_2:<11} {q.date.strftime('%d.%m.%Y'):<8} {q.band:<5} {q.mode:<5} {q.report}"
