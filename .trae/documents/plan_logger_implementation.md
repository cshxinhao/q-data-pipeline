# Implementation Plan - Add Logger

We will implement a centralized logging module in `src/logger.py` and replace existing `print` statements in the codebase with proper logging calls.

## User Review Required

> [!IMPORTANT]
> The log files will be stored in the `./logs` directory relative to the project root.
> The default log level will be set to `INFO`.

## Proposed Changes

### 1. Implement `src/logger.py`

- Create a `setup_logger` function or a configured `logger` instance.
- Ensure the `./logs` directory exists.
- Configure `FileHandler` to write logs to `./logs/app.log` (or similar).
- Configure `StreamHandler` to output logs to the console.
- Set a standard log format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`.

### 2. Update `src/vendors/tushare/cleaner.py`

- Import `logger` from `src.logger`.
- Replace `print` statements with `logger.info`, `logger.warning`, or `logger.error`.

### 3. Update `src/vendors/tushare/downloader.py`

- Import `logger` from `src.logger`.
- Replace `print` statements with `logger.info`, `logger.warning`, or `logger.error`.

## Verification Plan

### Automated Tests
- None planned as this is a refactor of logging.

### Manual Verification
- Run one of the tushare scripts (e.g., `python -m src.vendors.tushare.cli download trade-cal --start 20240101 --end 20240105`) and verify:
    - Logs appear in the console.
    - A log file is created in `./logs`.
    - The content of the logs matches the expected output.
