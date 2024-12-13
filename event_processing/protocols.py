from typing import Protocol, Self

from pandas import Series

from event_processing.context import BakingContext


class BakingState(Protocol):
    def process_event(self, context: BakingContext, event: Series) -> Self:
        pass
