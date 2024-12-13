import datetime

from event_processing.custom_types import EventProcessingResult


class BakingContext:
    def __init__(self, oven: str, oven_number: int, total_ovens: int) -> None:
        self._oven = oven
        self._oven_number = oven_number
        self._total_ovens = total_ovens
        self._start_time: datetime.datetime | None = None
        self._end_time: datetime.datetime | None = None
        self._program: int | None = None

    @property
    def result(self) -> EventProcessingResult:
        if self._start_time and self._end_time:
            return {
                "Дата": self._start_time.date(),
                "Печь": self._oven,
                "Время старта": self._start_time,
                "Время завершения": self._end_time,
                "Номер программы выпечки": self._program,
                "Номер духовки": self._oven_number,
                "Количество духовок": self._total_ovens,
                "Длительность": self._end_time - self._start_time,
            }
        return None

    def reset(self) -> None:
        self._start_time = None
        self._end_time = None
        self._program = None

    def set_start(self, time: datetime.datetime, program: int) -> None:
        self._start_time = time
        self._program = program

    def set_end(self, time: datetime.datetime) -> None:
        self._end_time = time
