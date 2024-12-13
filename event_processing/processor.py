import pandas as pd
from pandas import Series

from event_processing.context import BakingContext
from event_processing.protocols import BakingState
from event_processing.states import InitialState


class BakingProcessor:
    def __init__(self):
        self._context: BakingContext | None = None
        self._state: BakingState = InitialState()
        self._results: list[dict] = []

    def process_event(self, event: Series) -> None:
        if self._context is None:
            self._context = BakingContext(
                event["Печь"],
                event["Номер духовки"],
                event["Количество духовок"],
            )
        self._state = self._state.process_event(self._context, event)
        if self._context.result and isinstance(self._state, InitialState):
            self._results.append(self._context.result)
            self._context.reset()

    def get_results(self) -> pd.DataFrame:
        return pd.DataFrame(self._results)


def process_baking_log(input_file: str, output_file: str) -> None:
    raw_data = pd.read_csv(input_file, sep=";", parse_dates=["Дата"], dayfirst=True)
    prepare_data = raw_data[raw_data["ID события"].isin([15, 1, 20, 21, 16, 17, 18, 8])]

    processor = BakingProcessor()
    for _, row in prepare_data.iterrows():
        processor.process_event(row)
    result_df = processor.get_results()
    result_df.to_csv(output_file, index=False, sep=";")
