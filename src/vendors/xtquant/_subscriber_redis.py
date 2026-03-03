from functools import partial
import time
import multiprocessing as mp
import queue
import polars as pl
from pathlib import Path
from datetime import datetime
from xtquant import xtdata
import redis  # 新增：Redis 客户端
import structlog  # 新增：增强日志
from prometheus_client import start_http_server, Gauge  # 新增：Prometheus 监控
import threading  # 新增：用于定时 flush

# Config
logger = structlog.get_logger()  # 使用 structlog
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ]
)
TODAY = datetime.now().strftime("%Y%m%d")
SAVE_DIR = Path(rf"D:\data_warehouse\vendor_realtime_subscription\xtquant\{TODAY}")
SAVE_DIR.mkdir(parents=True, exist_ok=True)
BATCH_SIZE = 50000
MIN_FLUSH_SIZE = 1000  # 新增：最小 flush 大小，减少小文件
FLUSH_INTERVAL = 5  # 新增：定时 flush 间隔（秒）

# Prometheus 指标（新增）
queue_length = Gauge("queue_length", "Current length of the tick queue")
record_count = Gauge("record_count", "Total records processed")


class DataConsumer:
    """消费者进程类：负责从队列取数据并写入 Parquet"""

    def __init__(self, redis_client, save_dir):
        self.redis = redis_client  # 改为 Redis
        self.save_dir = save_dir
        self.buffer = []
        self.timer = None  # 新增：定时器

    def run(self):
        logger.info(f"[Consumer] Started, saving to {self.save_dir}")
        start_http_server(8000)  # 新增：暴露 Prometheus 指标（端口 8000）

        # 新增：启动定时 flush
        self.schedule_flush()

        while True:
            try:
                # 从 Redis 阻塞拉取数据，超时 1 秒
                data = self.redis.blpop("tick_queue", timeout=1)
                if data is None:
                    continue  # 无数据，继续

                # data 是元组 (queue_name, value)，取 value 并解码
                record = eval(
                    data[1].decode("utf-8")
                )  # 假设使用 str 存储，实际可改 JSON

                # 检查停止信号 (特殊记录，如 {'stop': True})
                if isinstance(record, dict) and record.get("stop"):
                    self.flush()
                    logger.info("[Consumer] Received stop signal, exiting.")
                    break

                self.buffer.append(record)

                # 更新指标
                queue_length.set(self.redis.llen("tick_queue"))
                record_count.inc()

                # 达到批次大小，写入磁盘
                if len(self.buffer) >= BATCH_SIZE:
                    self.flush()

            except redis.exceptions.TimeoutError:  # 对应 queue.Empty
                # 队列空了，如果有缓冲数据且达到最小大小，写入
                if len(self.buffer) >= MIN_FLUSH_SIZE:
                    self.flush()
                continue
            except Exception as e:
                logger.error(f"[Consumer] Error: {e}")

    def schedule_flush(self):
        # 新增：定时检查 flush
        if self.buffer and len(self.buffer) >= MIN_FLUSH_SIZE:
            self.flush()
        self.timer = threading.Timer(FLUSH_INTERVAL, self.schedule_flush)
        self.timer.start()

    def flush(self):
        if not self.buffer:
            return
        try:
            df = pl.from_records(self.buffer)
            ts = datetime.now().strftime("%H%M%S_%f")
            file_path = self.save_dir / f"tick_{ts}.parquet"
            df.write_parquet(file_path, compression="zstd")
            logger.info(
                f"[Consumer] Saved {len(self.buffer)} records to {file_path.name}"
            )
            self.buffer = []
        except Exception as e:
            logger.error(f"[Consumer] Flush error: {e}")


class DataProducer:
    """生产者类：负责订阅行情并将数据放入队列"""

    def __init__(self, redis_client):
        self.redis = redis_client  # 改为 Redis
        self.count = 0

    def callback(self, datas):
        logger.debug(f"Callback received {len(datas)} records")
        try:
            for stock_code, tick_data in datas.items():
                record = serialize(stock_code, tick_data)
                # 放入 Redis (使用 str 存储，实际可改 JSON)
                self.redis.rpush("tick_queue", str(record))
                self.count += 1

            if self.count % 100000 == 0:
                logger.info(f"[Producer] Received {self.count} ticks...")

            # 更新指标
            queue_length.set(self.redis.llen("tick_queue"))

        except Exception as e:
            logger.error(f"[Producer] Callback error: {e}")

    def start_subscription(self):

        # code_list = ["SH", "SZ"]
        code_list = xtdata.get_stock_list_in_sector("沪深A股")

        self.subscription_id = xtdata.subscribe_whole_quote(
            code_list=code_list,
            callback=self.callback,
        )
        logger.info("[Producer] Subscription started.")

    def stop_subscription(self):
        xtdata.unsubscribe_quote(self.subscription_id)
        logger.info("[Producer] Subscription stopped.")


def serialize(stock_code, tick_data):
    return {
        "stock_code": stock_code,
        "time": tick_data.get("time"),
        "lastPrice": tick_data.get("lastPrice"),
        "open": tick_data.get("open"),
        "high": tick_data.get("high"),
        "lastClose": tick_data.get("lastClose"),
        "amount": tick_data.get("amount"),
        "volume": tick_data.get("volume"),
        "pvolume": tick_data.get("pvolume"),
        "stockStatus": tick_data.get("stockStatus"),
        "openInt": tick_data.get("openInt"),
        "transactionNum": tick_data.get("transactionNum"),
        "lastSettlementPrice": tick_data.get("lastSettlementPrice"),
        "settlementPrice": tick_data.get("settlementPrice"),
        "pe": tick_data.get("pe"),
        "askPrice1": tick_data.get("askPrice")[0],
        "askPrice2": tick_data.get("askPrice")[1],
        "askPrice3": tick_data.get("askPrice")[2],
        "askPrice4": tick_data.get("askPrice")[3],
        "askPrice5": tick_data.get("askPrice")[4],
        "bidPrice1": tick_data.get("bidPrice")[0],
        "bidPrice2": tick_data.get("bidPrice")[1],
        "bidPrice3": tick_data.get("bidPrice")[2],
        "bidPrice4": tick_data.get("bidPrice")[3],
        "bidPrice5": tick_data.get("bidPrice")[4],
        "askVol1": tick_data.get("askVol")[0],
        "askVol2": tick_data.get("askVol")[1],
        "askVol3": tick_data.get("askVol")[2],
        "askVol4": tick_data.get("askVol")[3],
        "askVol5": tick_data.get("askVol")[4],
        "bidVol1": tick_data.get("bidVol")[0],
        "bidVol2": tick_data.get("bidVol")[1],
        "bidVol3": tick_data.get("bidVol")[2],
        "bidVol4": tick_data.get("bidVol")[3],
        "bidVol5": tick_data.get("bidVol")[4],
        "volRatio": tick_data.get("volRatio"),
        "speed1Min": tick_data.get("speed1Min"),
        "speed5Min": tick_data.get("speed5Min"),
    }


def main():
    # Redis 连接（新增）
    r = redis.Redis(host="localhost", port=6379, db=0)

    # 清空队列（可选，测试时用）
    r.delete("tick_queue")

    # Consumer
    consumer = DataConsumer(r, SAVE_DIR)
    p_consumer = mp.Process(target=consumer.run)
    p_consumer.start()

    # Producer
    producer = DataProducer(r)
    producer.start_subscription()

    # 主线程监控
    client = xtdata.get_client()
    try:
        while True:
            time.sleep(1)
            if not client.is_connected():
                raise Exception("Client is not connected")
            if not p_consumer.is_alive():
                logger.error("[Main] Consumer process died. Restarting...")
                p_consumer = mp.Process(target=consumer.run)
                p_consumer.start()
    except KeyboardInterrupt:
        logger.info("[Main] KeyboardInterrupt received. Stopping...")
        producer.stop_subscription()
        # 发送停止信号到 Redis
        r.rpush("tick_queue", str({"stop": True}))
        p_consumer.join(timeout=5)
        logger.info("[Main] All processes stopped.")
