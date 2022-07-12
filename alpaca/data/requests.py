from datetime import datetime
from typing import Optional, List, Union

from alpaca.common.models import NonEmptyRequest
from alpaca.data import TimeFrame, Adjustment, DataFeed, Exchange


def convert_datetime_to_iso_8601_with_z_suffix(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


class BaseGetBarsRequest(NonEmptyRequest):
    """
    A base request object for retrieving bar data for securities. You most likely should not use this directly and instead
    use the asset class specific request objects.


    Attributes:
        symbol_or_symbols (Union[str, List[str]]): The security or multiple security ticker identifiers
        timeframe (TimeFrame): The period over which the bars should be aggregated. (i.e. 5 Min bars, 1 Day bars)
        start (Optional[datetime], optional): The beginning of the time interval for desired data. Defaults to None.
        end (Optional[datetime], optional): The beginning of the time interval for desired data. Defaults to None.
        limit (Optional[int], optional): Upper limit of number of data points to return. Defaults to None.
    """

    symbol_or_symbols: Union[str, List[str]]
    timeframe: TimeFrame
    start: Optional[Union[datetime, str]]
    end: Optional[Union[datetime, str]]
    limit: Optional[int]

    # Allows TimeFrame as a non-pydantic BaseModel field
    class Config:
        arbitrary_types_allowed = True


class GetStockBarsRequest(BaseGetBarsRequest):
    """
    The request model for retrieving bar data for equities.

    See BaseGetBarsRequest for more information on available parameters.

    Attributes:
        adjustment (Optional[Adjustment], optional): The type of corporate action data normalization. Defaults to None.
        feed (Optional[DataFeed], optional): The equity data feed to retrieve from. Defaults to None.
    """

    adjustment: Optional[Adjustment]
    feed: Optional[DataFeed]


class GetCryptoBarsRequest(BaseGetBarsRequest):
    """
    The request model for retrieving bar data for cryptocurrencies.

    See BaseGetBarsRequest for more information on available parameters.

    Attributes:
        exchanges (Optional[List[Exchange]]): The crypto exchanges to retrieve bar data from. Defaults to None.
    """

    exchanges: Optional[List[Exchange]]
