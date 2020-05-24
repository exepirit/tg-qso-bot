from datetime import date
from dataclasses import dataclass


@dataclass()
class Qso:
    call_sign_1: str
    call_sign_2: str
    date: date
    band: str
    mode: str
    report: str
