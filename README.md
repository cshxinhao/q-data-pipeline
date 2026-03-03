# q-data-pipeline

**q-data-pipeline** is a robust financial data pipeline designed to fetch, clean, and validate market data from various vendors, with a primary focus on the Chinese stock market (A-shares). It provides a unified interface for managing data from sources like **Tushare** and **XtQuant**, ensuring high-quality data for quantitative analysis and trading.

## Features

- **Multi-Vendor Support**:
  - **Tushare**: Comprehensive historical data for Chinese markets.
  - **XtQuant**: Real-time and historical data integration for quantitative trading.
  - **Futu**: (Work in Progress) Integration with Futu Securities.

- **Automated Workflows**:
  - **Downloading**: Efficiently fetch raw data including daily bars, trade calendars, tickers, and adjustment factors.
  - **Cleaning**: Standardize and process raw data into a consistent, analysis-ready format.
  - **Validation**: rigorous data integrity checks to detect duplicates, nulls, outliers, and logical inconsistencies.

- **Modular Architecture**: Clean separation of concerns with vendor-specific modules, common utilities, and a dedicated checker module.

## Project Structure

```
q-data-pipeline/
├── src/
│   ├── vendors/        # Vendor-specific implementations (tushare, xtquant, futu)
│   ├── checker/        # Data validation and quality assurance logic
│   ├── common/         # Shared utilities and schemas
│   ├── database.py     # Database interaction layer
│   └── logger.py       # Logging configuration
├── scripts/            # Shell and Batch scripts for automation
├── requirements/       # Dependency files for different environments
└── tests/              # Unit and integration tests
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- A Tushare account and API Token (if using Tushare)
- XtQuant client installed (if using XtQuant)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/q-data-pipeline.git
    cd q-data-pipeline
    ```

2.  **Set up a virtual environment (recommended):**
    
    ```bash
    conda create --prefix venv/tushare
    conda create --prefix venv/xt
    ```
    
3.  **Install dependencies:**
    Select the requirements file based on your needs:
    ```bash
    # For Tushare support
    conda activate venv/tushare
    pip install -r requirements/env_tushare.txt
    
    # For XtQuant support
    conda activate venv/xt
    pip install -r requirements/env_xtquant.txt
    
    # For all features (check requirements/env_checker.txt, etc.)
    ```

### Configuration

1.  Copy the example environment file:
    ```bash
    cp .env.example .env
    ```

2.  Edit `.env` and configure your settings:
    ```ini
    TUSHARE_TOKEN=your_actual_tushare_token
    DATA_RAW_DIR=./data/raw
    DATA_CLEAN_DIR=./data/clean
    ```

## Usage

The project uses command-line interfaces (CLI) for different modules. You can run them as Python modules or use the provided scripts.

### Tushare

**Downloading Data:**
```bash
# Download daily bars for a specific date range
python -m src.vendors.tushare.cli download 1day-bar --start 20230101 --end 20231231 --replace true

# Download trade calendar
python -m src.vendors.tushare.cli download trade-cal --start 20230101 --end 20231231
```

**Cleaning Data:**
```bash
# Clean trade calendar
python -m src.vendors.tushare.cli clean trade-cal
```

**Using Scripts:**
Convenience scripts are located in the `scripts/` directory:
- `run_tushare_download.bat`: Automates the download process.
- `run_tushare_clean.bat`: Automates the cleaning process.

### XtQuant

**Downloading Data:**
```bash
# Download sector data
python -m src.vendors.xtquant.cli download sector-data

# Download 1-day and 1-min bars
python -m src.vendors.xtquant.cli download bar
```

### Data Validation (Checker)

Ensure your data quality by running the checker module:

```bash
# Check for duplicates
python -m src.checker.cli check duplicate --market China --vendor tushare

# Check for null values
python -m src.checker.cli check null --market China --vendor tushare

# Check for logic inconsistencies (e.g., High < Low)
python -m src.checker.cli check logic-consistency --market China --vendor tushare
```

## Contributing

Contributions are welcome! Please submit a Pull Request or open an Issue to discuss any changes.

## License

[MIT License](LICENSE)