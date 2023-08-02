# FinTable - Financial Statement Extraction Tool

## Overview

FinTable is a Python-based financial statement extraction tool designed to extract financial data from annual reports in PDF format. It utilizes various libraries and regex patterns to parse financial tables and produce structured datasets for statements of financial position (SOFP), statements of profit or loss (SOPL), and statements of cash flow (SOCF). This tool simplifies the process of extracting financial information and saves the extracted data as CSV files.

## Features

- Extraction of financial tables from PDF annual reports.
- Identification of relevant financial statements based on keywords and regex patterns.
- Clean-up and organization of extracted financial data.
- Support for extracting financial statements from both regular companies and banks (with customizable keyword lists).

## Requirements

To use FinTable, you need the following dependencies:

- Python 3.x
- Libraries:
  - camelot
  - PyMuPDF
  - pandas

You can install these dependencies using pip:

```bash
pip install camelot pymupdf pandas
```

## Usage

To use FinTable, you can follow the steps below:

1. Import the required libraries and classes:

```python
import camelot
import fitz
import re
import pandas as pd
from datetime import datetime
```

2. Instantiate the `AnnualReport` class with the path to your PDF annual report:

```python
from FinTable import AnnualReport

report_file = "path/to/your_annual_report.pdf"
annual_report = AnnualReport(report_file)
```

3. Extract financial statements:

```python
# Extract Statement of Financial Position (SOFP)
sofp_data = annual_report.report("SOFP")

# Extract Statement of Profit or Loss (SOPL)
sopl_data = annual_report.report("SOPL")

# Extract Statement of Cash Flow (SOCF)
socf_data = annual_report.report("SOCF")
```

4. Optionally, you can save the extracted data as CSV files:

```python
# Save Statement of Financial Position (SOFP) as a CSV file
annual_report.save_report("SOFP")

# Save Statement of Profit or Loss (SOPL) as a CSV file
annual_report.save_report("SOPL")

# Save Statement of Cash Flow (SOCF) as a CSV file
annual_report.save_report("SOCF")
```

## Customization

FinTable allows you to customize the keyword lists used for identifying relevant financial statements, especially if the company is a bank. You can do this by modifying the `features` attribute in the `AnnualReport` class based on your specific requirements.

```python
# Example customization for bank's financial statements
annual_report = AnnualReport(report_file, bank=True)

# Customization for regular company's financial statements (default)
annual_report = AnnualReport(report_file, bank=False)
```

Please note that the accuracy of the financial statement extraction heavily depends on the quality and structure of the PDF annual report. Ensure that the PDF format is consistent and well-structured for better extraction results.

## License

FinTable is released under the [MIT License](https://opensource.org/licenses/MIT).

## Contributions

We welcome contributions to FinTable. If you encounter any issues or have suggestions for improvements, please create an issue on our [GitHub repository](https://github.com/lazyaccountant/FinTable).

## Contact

For any questions or inquiries, please contact me at [enyocollins@gmail.com](mailto:enyocollins@gmail.com).