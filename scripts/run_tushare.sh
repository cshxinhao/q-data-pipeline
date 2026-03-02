#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# Assuming the script is in scripts/ and project root is one level up
PROJECT_ROOT="$SCRIPT_DIR/.."

# Change to project root
cd "$PROJECT_ROOT" || exit

# Set date range for demonstration
START_DATE="20230101"
END_DATE="20230131"

echo "Running Tushare pipeline from $PROJECT_ROOT"

# 1. Download Trade Calendar
echo "Step 1: Downloading trade calendar ($START_DATE - $END_DATE)..."
python -m src.vendors.tushare.cli download trade-cal --start "$START_DATE" --end "$END_DATE"

# 2. Download Ticker Mapper
echo "Step 2: Downloading ticker mapper..."
python -m src.vendors.tushare.cli download ticker-mapper

# 3. Download 1-Day Bar Prices
echo "Step 3: Downloading 1-day bar prices ($START_DATE - $END_DATE)..."
python -m src.vendors.tushare.cli download 1day-bar-price --start "$START_DATE" --end "$END_DATE" --replace

# 4. Clean 1-Day Bar Prices
echo "Step 4: Cleaning 1-day bar prices ($START_DATE - $END_DATE)..."
python -m src.vendors.tushare.cli clean 1day-bar-price --start "$START_DATE" --end "$END_DATE" --replace

echo "Tushare pipeline completed."
