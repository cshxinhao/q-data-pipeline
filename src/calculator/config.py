from pathlib import Path


class CalculatorOutputPath:
    def __init__(
        self,
    ):
        self.base_dir = self._ensure_dir(Path(r"D:\data_warehouse\clean_data"))

    @property
    def ml_common_data(self):
        return self._ensure_dir(self.base_dir / "ml_common_data")

    def _ensure_dir(self, path: Path):
        path.mkdir(parents=True, exist_ok=True)
        return path
