import requests
from typing import List, Dict, Optional
from datetime import date, datetime
from bs4 import BeautifulSoup
from tg_qso_bot.models import Qso
from .source import QsoSource
from .exceptions import ServerResponseError, ParsingError

HAMLOG_URL = "https://hamlog.online"
HAMLOG_USERAGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"


class _HamlogSession:
    CSRF_TOKEN_FIELD = "csrf-progress"

    def __init__(self, session: requests.Session = None, url: str = HAMLOG_URL, default_headers=None):
        if default_headers is None:
            default_headers = {}
        self._url = url
        self._headers = {"User-Agent": self.CSRF_TOKEN_FIELD, **default_headers}
        self._token: Optional[str] = None
        self._session: requests.Session = session or requests.Session()

    def retrieve_token(self) -> str:
        response = self._session.request("GET", self._url, headers=self._headers)
        if not response.ok:
            raise ServerResponseError(self._url, response.status_code)
        soup = BeautifulSoup(response.text, "html.parser")
        form = soup.find("form", {"action": "/progress.php"})
        if not form:
            raise KeyError("Form with CSRF token not found")
        csrf_field = form.find_next("input", {"name": "csrf-progress"})
        return csrf_field["value"]

    @property
    def token(self) -> str:
        if not self._token:
            self._token = self.retrieve_token()
        return self._token


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
        qso = self._parse_qso_list(callsign, page)
        return qso[:limit]

    def _get_qso_log_page(self, callsign: str):
        with requests.Session() as session:
            hamlog_session = _HamlogSession(session)
            data = {"callsign": callsign, "csrf-progress": hamlog_session.token}
            response = session.post(f"{self._url}/progress.php", headers=self._headers, data=data)
        if not response.ok:
            raise ServerResponseError(self._url, response.status_code)
        return response.text

    def _parse_qso_list(self, callsign_1: str, data: str) -> List[Qso]:
        # LEGACY CODE!!! Need to rewrite to a modern library
        soup = BeautifulSoup(data, "html.parser")
        result = []
        table = soup.find("table", {"id": "qsos"})
        if not table:
            raise ParsingError("Could not find QSO table", data)
        if thead := table.find("thead"):
            thead.decompose()
        if tfoot := table.find("tfoot"):
            tfoot.decompose()
        for tr in table.find_all("tr"):
            fields = [f.renderContents().strip().decode("utf-8") for f in tr.find_all("td")]
            datetime.strptime(fields[0], "%d %b %Y").date()
            qso = Qso(
                call_sign_1=callsign_1,
                call_sign_2=fields[1],
                date=datetime.strptime(fields[0], "%d %b %Y").date(),
                band=fields[2],
                mode=fields[3],
                report="-",
            )
            result.append(qso)
        return result
