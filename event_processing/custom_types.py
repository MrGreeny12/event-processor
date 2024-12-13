import datetime

EventProcessingResult = (
    dict[str, str | int | datetime.timedelta | datetime.date | None] | None
)
