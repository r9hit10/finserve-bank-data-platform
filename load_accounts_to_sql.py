import pyodbc
import pandas as pd
import numpy as np

def clean_value(val):
    if pd.isna(val):
        return None
    return val

conn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=localhost\\SQLEXPRESS;"
    "Database=FinServeDB;"
    "Trusted_Connection=yes;"
)
conn = pyodbc.connect(conn_str)
print("Connected successfully!")

accounts_df = pd.read_csv("accounts_raw.csv")
accounts_df["OpenDate"] = pd.to_datetime(accounts_df["OpenDate"], errors="coerce")
accounts_df["ModifiedDate"] = pd.to_datetime(accounts_df["ModifiedDate"], errors="coerce")

cursor = conn.cursor()
success_count = 0
fail_count = 0
failed_rows = []

for index, row in accounts_df.iterrows():
    try:
        cursor.execute(
            """
            INSERT INTO Accounts (AccountID, CustomerID, AccountNumber, AccountType, OpenDate, Balance, Status, ModifiedDate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            clean_value(row.AccountID), clean_value(row.CustomerID), clean_value(row.AccountNumber),
            clean_value(row.AccountType), clean_value(row.OpenDate), clean_value(row.Balance),
            clean_value(row.Status), clean_value(row.ModifiedDate)
        )
        conn.commit()
        success_count += 1
    except Exception as e:
        fail_count += 1
        failed_rows.append((row.AccountID, str(e)))

print(f"Success: {success_count}, Failed: {fail_count}")
print("Sample failures:", failed_rows[:5])