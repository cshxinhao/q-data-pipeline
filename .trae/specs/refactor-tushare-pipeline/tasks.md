# Tasks

- [x] Task 1: Setup Environment and Dependencies
  - [x] SubTask 1.1: Add `click` and `python-dotenv` to `requirements/env_tushare.txt` and other vendor requirements if needed.
  - [x] SubTask 1.2: Create a template `.env.example` with necessary variables (e.g., `TUSHARE_TOKEN`, `DATA_RAW_DIR`, `DATA_CLEAN_DIR`).

- [x] Task 2: Refactor Tushare Configuration
  - [x] SubTask 2.1: Modify `src/vendors/tushare/config.py` to load configuration from environment variables.
  - [x] SubTask 2.2: Ensure paths are dynamically constructed based on the base directories.

- [x] Task 3: Refactor Tushare Downloader
  - [x] SubTask 3.1: Remove CLI logic (`main` function and `argparse`) from `src/vendors/tushare/downloader.py`.
  - [x] SubTask 3.2: Ensure all download functions are properly exported and accept parameters.

- [x] Task 4: Refactor Tushare Cleaner
  - [x] SubTask 4.1: Ensure `clean_1day_bar` and other cleaning functions in `src/vendors/tushare/cleaner.py` are properly exported.
  - [x] SubTask 4.2: Add error handling for missing files.

- [x] Task 5: Implement Tushare CLI
  - [x] SubTask 5.1: Create `src/vendors/tushare/cli.py` using `click`.
  - [x] SubTask 5.2: Implement `download` command group with subcommands for different data types.
  - [x] SubTask 5.3: Implement `clean` command group with subcommands.

- [x] Task 6: Initialize Other Vendors (XTQuant, Futu)
  - [x] SubTask 6.1: Create directory structure for `src/vendors/xtquant` if not complete (add `cli.py`, `config.py`, `cleaner.py`).
  - [x] SubTask 6.2: Create directory structure for `src/vendors/futu` (add `cli.py`, `downloader.py`, `config.py`, `cleaner.py`).
  - [x] SubTask 6.3: Create basic CLI templates for these vendors.

- [x] Task 7: Update Scripts
  - [x] SubTask 7.1: Update `scripts/run_tushare.sh` to use the new CLI command.
