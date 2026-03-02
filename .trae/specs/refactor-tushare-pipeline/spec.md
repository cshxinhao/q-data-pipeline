# Refactor Data Pipeline for Tushare and other vendors

## Why
The current implementation of the Tushare data pipeline is a simple script with hardcoded paths and mixed responsibilities. The user wants a robust, modular pipeline structure that can be easily extended to other vendors like XTQuant and Futu. Each vendor requires its own environment configuration and CLI commands for downloading and cleaning data.

## What Changes
- **Refactor Tushare Module**:
  - Move CLI logic from `downloader.py` to `cli.py` using `click` for a better CLI experience.
  - Separate download and cleaning logic clearly.
  - Update `config.py` to use environment variables instead of hardcoded paths.
- **Standardize Vendor Structure**:
  - Create a consistent directory structure for `xtquant` and `futu` vendors (cli, downloader, cleaner, config).
- **Environment Management**:
  - Use `.env` files for configuration.
  - Update `requirements` to include necessary packages (`click`, `python-dotenv`).

## Impact
- **Affected Specs**: Data ingestion and processing capabilities.
- **Affected Code**: `src/vendors/tushare/`, `src/vendors/xtquant/`, `src/vendors/futu/`.
- **New Dependencies**: `click`, `python-dotenv`.

## ADDED Requirements
### Requirement: Unified CLI Interface
The system SHALL provide a CLI command `python -m src.vendors.<vendor>.cli` with subcommands `download` and `clean`.

#### Scenario: Download Data
- **WHEN** user runs `python -m src.vendors.tushare.cli download --type 1day-bar-price --start 2023-01-01 --end 2023-01-31`
- **THEN** the system downloads the data to the configured raw data directory.

#### Scenario: Clean Data
- **WHEN** user runs `python -m src.vendors.tushare.cli clean --type 1day-bar-price --date 2023-01-01`
- **THEN** the system reads raw data, cleans it, and saves it to the configured clean data directory.

### Requirement: Environment Isolation
Each vendor SHALL have its own configuration for API tokens and data paths, loadable from environment variables or `.env` files.

## MODIFIED Requirements
### Requirement: Tushare Script Improvement
The existing `downloader.py` script SHALL be refactored to remove CLI logic and focus solely on download implementation. The `cleaner.py` SHALL be integrated into the new CLI.
