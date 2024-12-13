from pandas import Series

from event_processing.context import BakingContext
from typing import Self


class InitialState:
    def process_event(self, context: BakingContext, event: Series) -> Self:
        """
        Состояние выбора программы. Начало процесса выпечки.
        Args:
            context: Baking context instance
            event: Event data from input file

        Returns: Initial state instance

        """
        if event["ID события"] == 15:
            context.reset()
            return PreheatingState()
        return self


class PreheatingState:
    def process_event(self, context: BakingContext, event: Series) -> Self:
        """
        Состояние завершения преднагрева печки.
        Args:
            context: Baking context instance
            event: Event data from input file

        Returns: Preheating state instance

        """
        if event["ID события"] == 1:
            return DoorControlState()
        return self


class DoorControlState:
    def process_event(self, context: BakingContext, event: Series) -> Self:
        """
        Состояние открытия/закрытия дверей печки.
        Args:
            context: Baking context instance
            event: Event data from input file

        Returns: Door control state instance

        """
        if event["ID события"] in [20, 21]:
            return BakingStartState()
        return self


class BakingStartState:
    def process_event(self, context: BakingContext, event: Series) -> Self:
        """
        Состояние начала выпекания.
        Args:
            context: Baking context instance
            event: Event data from input file

        Returns: Baking start state instance

        """
        if event["ID события"] == 16:
            context.set_start(event["Дата"], event["Программа"])
            return BakingEndState()
        return self


class BakingEndState:
    def process_event(self, context: BakingContext, event: Series) -> Self:
        """
        Состояние завершения или прерывания выпекания.
        Args:
            context: Baking context instance
            event: Event data from input file

        Returns: Baking end state instance

        """
        if event["ID события"] in [17, 18, 8]:
            context.set_end(event["Дата"])
            return InitialState()
        return self
