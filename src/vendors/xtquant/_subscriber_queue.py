from functools import partial
import time
import multiprocessing as mp
import queue
import polars as pl
from pathlib import Path
from datetime import datetime
from xtquant import xtdata
from src.logger import setup_logger

# Config
logger = setup_logger(
    name="subscribe",
    log_file="subscribe.log",
    level="INFO",
)
TODAY = datetime.now().strftime("%Y%m%d")
SAVE_DIR = Path(rf"D:\data_warehouse\vendor_realtime_subscription\xtquant\{TODAY}")
SAVE_DIR.mkdir(parents=True, exist_ok=True)
MAX_SIZE = 200000
BATCH_SIZE = 50000


class DataConsumer:
    """消费者进程类：负责从队列取数据并写入 Parquet"""

    def __init__(self, queue, save_dir):
        self.queue = queue
        self.save_dir = save_dir
        self.buffer = []

    def run(self):
        logger.info(f"[Consumer] Started, saving to {self.save_dir}")
        while True:
            try:
                # 阻塞获取数据，超时 1 秒以便检查停止信号
                data = self.queue.get(timeout=1.0)

                # 检查停止信号 (None)
                if data is None:
                    self.flush()
                    logger.info("[Consumer] Received stop signal, exiting.")
                    break

                self.buffer.append(data)

                # 达到批次大小，写入磁盘
                if len(self.buffer) >= BATCH_SIZE:
                    self.flush()

            except queue.Empty:
                # 队列空了，如果有缓冲数据也写入（防止收盘丢失）
                if self.buffer:
                    self.flush()
                continue
            except Exception as e:
                logger.error(f"[Consumer] Error: {e}")

    def flush(self):
        if not self.buffer:
            return
        try:
            df = pl.from_records(self.buffer)
            # 生成文件名：tick_时分秒_随机戳.parquet
            ts = datetime.now().strftime("%H%M%S_%f")
            file_path = self.save_dir / f"tick_{ts}.parquet"

            # 写入 Parquet，使用 ZSTD 压缩
            df.write_parquet(file_path, compression="zstd")
            logger.info(
                f"[Consumer] Saved {len(self.buffer)} records to {file_path.name}"
            )
            self.buffer = []
        except Exception as e:
            logger.error(f"[Consumer] Flush error: {e}")


class DataProducer:
    """生产者类：负责订阅行情并将数据放入队列"""

    def __init__(self, queue):
        self.queue = queue
        self.count = 0

    def callback(self, datas):
        """
        xtquant 回调函数
        :param datas: dict, key=stock_code, value=dict(fields)
        """
        logger.debug(f"Callback received {len(datas)} records")
        try:
            # 遍历全市场推送的数据
            for stock_code, tick_data in datas.items():
                # 数据清洗与展平 (关键步骤：深拷贝字段值)
                # 注意：xtquant 字段名可能是 'lastPrice', 'open', 'high' 等，需根据实际文档调整
                record = serialize(stock_code, tick_data)

                # 放入队列 (非阻塞，满则丢弃或报警，防止阻塞行情线程)
                try:
                    self.queue.put_nowait(record)
                    self.count += 1
                except mp.Queue.Full:
                    # 队列满了，说明写入速度跟不上接收速度
                    # 生产环境建议这里记录日志或发送报警
                    logger.warning("[Producer] Queue full, data lost")

            # 简单打印进度
            if self.count % 1000 == 0:
                logger.info(f"[Producer] Received {self.count} ticks...")

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
    code_list = xtdata.get_stock_list_in_sector("沪深A股")
    logger.info(f"{len(code_list)} Stock list: {code_list[:10]}")

    # Create a queue for inter-process communication
    q = mp.Queue(maxsize=MAX_SIZE)

    # Consumer
    consumer = DataConsumer(q, SAVE_DIR)
    p_consumer = mp.Process(target=consumer.run)
    p_consumer.start()

    # Producer
    producer = DataProducer(q)
    producer.start_subscription()

    # Keep the main thread running to keep the subscription active
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

        # Signal producer to stop
        producer.stop_subscription()
        # Signal consumer to stop, and save the remaining data
        q.put(None)
        p_consumer.join(timeout=5)

        logger.info("[Main] All processes stopped.")
