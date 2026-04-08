import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta

NIGERIAN_STATES = [
    "Lagos", "Abuja", "Kano", "Rivers", "Oyo", "Delta",
    "Anambra", "Enugu", "Ogun", "Kaduna", "Imo", "Borno"
]

FIRST_NAMES = [
    "Chukwuemeka", "Adaeze", "Oluwaseun", "Fatima", "Emeka",
    "Ngozi", "Babatunde", "Amina", "Ifeanyi", "Chidinma",
    "Tunde", "Blessing", "Uche", "Halima", "Obinna",
    "Seun", "Kemi", "Dele", "Ngozi", "Ahmed"
]

LAST_NAMES = [
    "Okonkwo", "Adeyemi", "Musa", "Okafor", "Bello",
    "Nwosu", "Ibrahim", "Eze", "Abubakar", "Osei",
    "Chukwu", "Alabi", "Okeke", "Suleiman", "Nwachukwu"
]

BANKS = ["Kuda", "Moniepoint", "GTBank", "Access Bank", "First Bank", "Zenith Bank", "UBA"]
TRANSACTION_TYPES = ["deposit", "withdrawal", "transfer", "airtime", "bill_payment", "pos"]
TRANSACTION_DESC = {
    "deposit": ["Salary payment", "Business income", "Wire transfer", "Cash deposit"],
    "withdrawal": ["ATM withdrawal", "Cash out", "Personal withdrawal"],
    "transfer": ["Send money", "Business payment", "Family support"],
    "airtime": ["MTN airtime", "Airtel airtime", "Glo airtime", "9mobile airtime"],
    "bill_payment": ["DSTV subscription", "EKEDC bill", "IKEDC bill", "Water bill"],
    "pos": ["Shoprite purchase", "Supermarket", "Restaurant", "Fuel station"]
}


def generate_customers(n=500):
    customers = []
    for i in range(n):
        customers.append({
            "customer_id": f"CUS{str(i+1).zfill(5)}",
            "full_name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            "age": random.randint(18, 65),
            "gender": random.choice(["Male", "Female"]),
            "state": random.choice(NIGERIAN_STATES),
            "bank": random.choice(BANKS),
            "account_type": random.choice(["savings", "current", "domiciliary"]),
            "account_balance": round(random.uniform(1000, 5000000), 2),
            "joined_date": (datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1500))).strftime("%Y-%m-%d"),
            "is_active": random.choice([1, 1, 1, 0])
        })
    return customers


def generate_transactions(customers, n=3000):
    transactions = []
    customer_ids = [c["customer_id"] for c in customers]
    for i in range(n):
        txn_type = random.choice(TRANSACTION_TYPES)
        amount = round(random.uniform(500, 500000), 2)
        is_fraud = 1 if amount > 400000 and random.random() < 0.15 else 0
        date = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 365))
        transactions.append({
            "transaction_id": f"TXN{str(i+1).zfill(6)}",
            "customer_id": random.choice(customer_ids),
            "transaction_type": txn_type,
            "amount": amount,
            "description": random.choice(TRANSACTION_DESC[txn_type]),
            "transaction_date": date.strftime("%Y-%m-%d"),
            "month": date.strftime("%B"),
            "month_num": date.month,
            "is_fraud": is_fraud,
            "status": random.choice(["success", "success", "success", "failed"])
        })
    return transactions


def create_database():
    print("Generating Nigerian banking data...")
    customers = generate_customers(500)
    transactions = generate_transactions(customers, 3000)

    customers_df = pd.DataFrame(customers)
    transactions_df = pd.DataFrame(transactions)

    conn = sqlite3.connect("naijabank.db")
    customers_df.to_sql("customers", conn, if_exists="replace", index=False)
    transactions_df.to_sql("transactions", conn, if_exists="replace", index=False)

    conn.execute("DROP VIEW IF EXISTS customer_summary")
    conn.execute("""
        CREATE VIEW customer_summary AS
        SELECT
            c.customer_id,
            c.full_name,
            c.state,
            c.bank,
            c.account_type,
            c.account_balance,
            c.age,
            c.gender,
            COUNT(t.transaction_id) as total_transactions,
            SUM(t.amount) as total_volume,
            SUM(CASE WHEN t.is_fraud = 1 THEN 1 ELSE 0 END) as fraud_count
        FROM customers c
        LEFT JOIN transactions t ON c.customer_id = t.customer_id
        GROUP BY c.customer_id
    """)

    conn.commit()
    conn.close()
    print("Database created: naijabank.db")
    print(f"   - {len(customers)} customers")
    print(f"   - {len(transactions)} transactions")


if __name__ == "__main__":
    create_database()