# encoding: utf-8

REQ_TRADE_CALENDAR_FIELDS = [
    "exchange",
    "calendar_date",
    "is_open",
    "pre_trade_date",
]

REQ_IDENTITY_FIELDS = [
    "symbol",
    "chinese_name",
    "english_name",
    "location",
    "sector",
    "industry",
    "board",
    "exchange",
    "list_date",
    "delist_date",
]

REQ_1D_BAR_FIELDS = [
    "datetime",
    "symbol",
    "open",
    "high",
    "low",
    "close",
    "vwap",
    "volume",
    "amount",
]

REQ_ADJ_FACTOR_FIELDS = [
    "datetime",
    "symbol",
    "adj_factor",
]


REQ_CAP_FIELDS = [
    "datetime",
    "symbol",
    "shares_out",
    "shares_float",
    "shares_ff",
    "cap_total",
    "cap_float",
    "cap_ff",
]

REQ_VALUATION_FIELDS = [
    "datetime",
    "symbol",
    "pe",
    "pb",
    "ps",
    "pe_ttm",
    "ps_ttm",
]
