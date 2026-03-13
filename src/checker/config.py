from pathlib import Path


class CheckerReportPath:
    def __init__(self, vendor: str = "tushare"):
        self.base_dir = self._ensure_dir(
            Path(r"D:\data_warehouse\vendor_check_report") / vendor
        )

    @property
    def network_delay(self):
        return self._ensure_dir(self.base_dir / "network_delay")

    def _ensure_dir(self, path: Path):
        path.mkdir(parents=True, exist_ok=True)
        return path
