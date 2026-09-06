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

customers_df = pd.read_csv("customers_raw.csv")
customers_df["CreatedDate"] = pd.to_datetime(customers_df["CreatedDate"], errors="coerce")
customers_df["ModifiedDate"] = pd.to_datetime(customers_df["ModifiedDate"], errors="coerce")

cursor = conn.cursor()
success_count = 0
fail_count = 0
failed_rows = []

for index, row in customers_df.iterrows():
    try:
        cursor.execute(
            """
            INSERT INTO Customers (CustomerID, FirstName, LastName, Email, Phone, City, State, CreatedDate, ModifiedDate, Status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            clean_value(row.CustomerID), clean_value(row.FirstName), clean_value(row.LastName),
            clean_value(row.Email), clean_value(row.Phone), clean_value(row.City), clean_value(row.State),
            clean_value(row.CreatedDate), clean_value(row.ModifiedDate), clean_value(row.Status)
        )
        conn.commit()
        success_count += 1
    except Exception as e:
        fail_count += 1
        failed_rows.append((row.CustomerID, str(e)))

print(f"Success: {success_count}, Failed: {fail_count}")
print("Sample failures:", failed_rows[:5])



