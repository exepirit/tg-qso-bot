import requests
from typing import List
from datetime import date
from bs4 import BeautifulSoup
from tg_qso_bot.models import Qso
from .source import QsoSource
from .exceptions import ServerResponseError, ParsingError

HAMLOG_URL = "https://hamlog.ru/#search"
HAMLOG_USERAGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0"


class HamlogQsoSource(QsoSource):
    def __init__(self, user_agent: str = None):
        self._url = HAMLOG_URL
        self._headers = {"User-Agent": user_agent or HAMLOG_USERAGENT}

    def get_qso_list(self, callsign: str, limit: int, skip: int = 0) -> List[Qso]:
        """
        Get QSO from HamLog.
        :param callsign: Callsign.
        :param limit: Requested QSO amount.
        :param skip: Indent from top of list.
        :return: List of QSOs.
        """
        page = self._get_qso_log_page(callsign)
        qso = self._parse_qso_list(page)
        return qso[:limit]

    def _get_qso_log_page(self, callsign: str):
        with requests.Session() as session:
            data = {"hiscall": "", "mycall": callsign}
            response = session.request("POST", self._url, headers=self._headers, data=data)
        if not response.ok:
            raise ServerResponseError(self._url, response.status_code)
        return response.text

    def _parse_qso_list(self, data: str) -> List[Qso]:
        # LEGACY CODE!!! Need to rewrite to a modern library
        soup = BeautifulSoup(data, "html.parser")
        result = []
        try:
            table = soup.find("table", {"id": "qsos"})
            table.find("thead").decompose()
            table.find("tfoot").decompose()
            for tr in table.find_all("tr"):
                fields = [f.renderContents().strip().decode("utf-8") for f in tr.find_all("td")]
                qso_date = [int(s) for s in fields[2].split(".")]  # 01.01.1970 -> [1, 1, 1970]
                qso = Qso(
                    call_sign_1=fields[0],
                    call_sign_2=fields[1],
                    date=date(*reversed(qso_date)),
                    band=fields[3],
                    mode=fields[4],
                    report=fields[5],
                )
                result.append(qso)
        except AttributeError as e:
            raise ParsingError(e)
        return result
