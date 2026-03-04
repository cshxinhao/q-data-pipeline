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

REQ_1MIN_BAR_FIELDS = [
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

REQ_TICK_QUOTE_FIELDS = [
    "datetime",
    "symbol",
    "stock_status",
    "last_price",
    "volume",
    "amount",
    "bid_px1",
    "bid_px2",
    "bid_px3",
    "bid_px4",
    "bid_px5",
    "bid_vol1",
    "bid_vol2",
    "bid_vol3",
    "bid_vol4",
    "bid_vol5",
    "ask_px1",
    "ask_px2",
    "ask_px3",
    "ask_px4",
    "ask_px5",
    "ask_vol1",
    "ask_vol2",
    "ask_vol3",
    "ask_vol4",
    "ask_vol5",
    "transaction_num",
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
