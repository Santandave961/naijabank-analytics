# 🏦 NaijaBank Analytics
### SQL-Powered Nigerian Banking Intelligence Dashboard

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![SQLite](https://img.shields.io/badge/Database-SQLite-orange)
![Plotly](https://img.shields.io/badge/Charts-Plotly-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

##  Live Demo
[NaijaBank Analytics on Streamlit Cloud](https://naijabank-analytics-hqryysvpstckcxpdx6gqrv.streamlit.app/)

---

##  Overview
NaijaBank Analytics is a SQL-powered business intelligence dashboard built with Python, SQLite, Pandas and Plotly. It simulates a Nigerian banking data warehouse with 500 customers and 3,000 transactions, providing deep insights into customer behaviour, transaction patterns, and fraud detection.

---

## Features
-  **KPI Metrics** — Total customers, transactions, volume and fraud cases
- **Customer Distribution** — Breakdown by state, bank and market share
- **Transaction Analysis** — Volume by type and monthly growth trends
- **Demographics** — Gender, age group and account type distribution
- **Fraud Analysis** — Fraud patterns by transaction type and state
- **Top Customers** — Ranked by total transaction volume
- **Data Explorer** — Filter and download raw transaction data as CSV
- **Dynamic Filters** — Filter by bank, state and gender

---

##  Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| SQLite | Database & SQL queries |
| Pandas | Data manipulation |
| Plotly | Interactive charts |
| Streamlit | Web dashboard |

---

##  Dataset
Synthetically generated Nigerian banking data including:
- **500 customers** across 12 Nigerian states
- **3,000 transactions** across 6 transaction types
- **7 banks** — Kuda, Moniepoint, GTBank, Access Bank, First Bank, Zenith Bank, UBA
- **Fraud flags** on suspicious high-value transactions

---

## Installation

```bash
# Clone the repository
git clone https://github.com/Santandave961/naijabank-analytics.git
cd naijabank-analytics

# Install dependencies
pip install -r requirements.txt

# Generate the database
python database.py

# Run the dashboard
streamlit run app.py
```

---

## Project Structure
```
naijabank-analytics/
├── app.py              # Streamlit dashboard
├── database.py         # Database generation script
├── naijabank.db        # SQLite database
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

##  Built For Nigerian Fintech
This project demonstrates SQL analytics and BI dashboard skills relevant to data roles at Nigerian fintech companies like Interswitch, Flutterwave, Kuda, and Moniepoint — where data-driven decision making is critical.

---

## Author
**Okparaji Wisdom**
- GitHub: [@Santandave961](https://github.com/Santandave961)

---

## 📄 License
MIT License — free to use and modify.
