from abc import ABC, abstractmethod
from typing import List
from tg_qso_bot.models import Qso


class QsoSource(ABC):
    """
    Storage adapter, from which QSO can be extracted.
    All implemented QSO sources inherit this class.
    """

    @abstractmethod
    def get_qso_list(self, callsign: str, limit: int, skip: int = 0) -> List[Qso]:
        """
        Get QSO list from a source.
        :param callsign: Callsign.
        :param limit: Requested QSO amount.
        :param skip: Indent from top of list.
        :return: List of QSOs.
        """
        raise NotImplementedError()
