# Website Health Check CSV Logger

Simple Python script that reads a CSV of website URLs, performs HTTP GET health checks, and writes results back to the CSV (adds Status, Response Time (ms), Checked At columns).

## Requirements
- Python 3.7+
- requests package

Install dependencies:
```powershell
python -m pip install requests
```

## CSV format
The CSV must include a header column named `website`. Example:
```csv
website,owner
https://example.com,Team A
https://api.example.com,Team B
```

## Usage
- Run with the default path embedded in the script:
```powershell
python healthcheck.py
```

- Run with a custom CSV path:
```powershell
python healthcheck.py "C:\path\to\websites_url.csv"
```

The script will replace the CSV with an updated file containing three extra columns:
- `Status` — "Healthy" or "Unhealthy (...)"  
- `Response Time (ms)` — numeric milliseconds or `N/A` on error  
- `Checked At` — ISO timestamp

## Notes
- Timeout is 5 seconds per request by default.
- The script writes to a temporary file then atomically replaces the original CSV.
- Make sure the CSV path is correct and the file is writable.
