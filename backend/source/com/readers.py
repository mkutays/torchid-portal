import sys
from datetime import date

from constants import LOGGER

from api.models import Event
from api.models import Category
from api.models import Athlete
from api.models import Record


class MessageReader:

    @staticmethod
    def check_sum(data: str):
        return hex(sum(data.encode('ascii')) % 256)

    @staticmethod
    def load(data: str) -> None:
        fdata, _comma, check_sum = data.strip().partition("*")
        expected_sum = hex(int(f"0x{check_sum}", 16))
        actual_sum = MessageReader.check_sum(fdata)
        if expected_sum == actual_sum:
            LOGGER.info("[READER] CheckSum Succeed!")
            msg_type, _comma, rdata = fdata.partition(",")
            return getattr(sys.modules[__name__], f"Message_{msg_type}").load(rdata)
        else:
            LOGGER.error(
                f"[READER] CheckSum Failed! Actual: {actual_sum}, Expected: {expected_sum}, Msg: {fdata}")


class Message_01:

    @classmethod
    def load(cls, data: str):
        LOGGER.info("[MSG-01] Parsing message...")
        card_str, _comma, rdata = data.partition(",")
        card_id = int(card_str)
        cp_cnt_str, _comma, rrdata = rdata.partition(",")
        cp_count = int(cp_cnt_str)
        val_list = rrdata.split(",")
        cp_list = val_list[0:cp_count]
        res_list = val_list[cp_count:]
        return cls(card_id, cp_list, res_list)

    def __convert_date(self, time_str):
        hour = time_str[0:2]
        mint = time_str[2:4]
        sec = time_str[4:6]
        milis = time_str[6:]
        return f"{hour}:{mint}:{sec} {milis}ms"

    def __init__(self, card_id: int, control_points: list, results: list) -> None:
        self.card_id = card_id
        self.control_points = control_points
        self.results = [self.__convert_date(time_str) for time_str in results]
        self.__event = None
        self.__category = None
        self.__athlete = None
        self.__process_data()

    def __process_data(self):
        self.__event = self.find_event()
        self.__category = self.find_category()
        self.__athlete = self.find_athlete()
        self.insert_data()

    def find_event(self):
        date_str = date.today().strftime("%Y-%m-%d")
        event = Event.objects.get(date=date_str)
        return event

    def find_category(self):
        category = Category.objects.get(
            event=self.__event, control_points=self.control_points)
        return category

    def find_athlete(self):
        athlete = Athlete.objects.get(
            category=self.__category, card_id=self.card_id)
        return athlete

    def insert_data(self):
        Record(athlete=self.__athlete, results=self.results).save()
