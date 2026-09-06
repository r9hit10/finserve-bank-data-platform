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

transactions_df = pd.read_csv("transactions_raw.csv")
transactions_df["TransactionDate"] = pd.to_datetime(transactions_df["TransactionDate"], errors="coerce")
transactions_df["CreatedDate"] = pd.to_datetime(transactions_df["CreatedDate"], errors="coerce")
transactions_df["ModifiedDate"] = pd.to_datetime(transactions_df["ModifiedDate"], errors="coerce")

cursor = conn.cursor()
success_count = 0
fail_count = 0
failed_rows = []

for index, row in transactions_df.iterrows():
    try:
        cursor.execute(
            """
            INSERT INTO Transactions (TransactionID, AccountID, TransactionType, Amount, TransactionDate, CreatedDate, ModifiedDate, Status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            clean_value(row.TransactionID), clean_value(row.AccountID), clean_value(row.TransactionType),
            clean_value(row.Amount), clean_value(row.TransactionDate), clean_value(row.CreatedDate),
            clean_value(row.ModifiedDate), clean_value(row.Status)
        )
        conn.commit()
        success_count += 1
    except Exception as e:
        fail_count += 1
        failed_rows.append((row.TransactionID, str(e)))

print(f"Success: {success_count}, Failed: {fail_count}")
print("Sample failures:", failed_rows[:5])