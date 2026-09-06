import pandas as pd
from faker import Faker

fake = Faker()
num_customers = 100000

customers = []

for i in range(1, num_customers + 1):
    customer = {
        "CustomerID": i,
        "FirstName": fake.first_name(),
        "LastName": fake.last_name(),
        "Email": fake.email(),
        "Phone": fake.phone_number(),
        "City": fake.city(),
        "State": fake.state(),
        "CreatedDate": fake.date_between(start_date="-3y", end_date="-1y"),
        "ModifiedDate": fake.date_between(start_date="-1y", end_date="today"),
        "Status": "Active"
    }
    customers.append(customer)

df = pd.DataFrame(customers)
import numpy as np

np.random.seed(42)  # so results are reproducible while we're learning

n = len(df)

# 1. Duplicate ~1% of CustomerIDs (pick random rows, duplicate them, append)
dup_indices = np.random.choice(df.index, size=int(n * 0.01), replace=False)
duplicates = df.loc[dup_indices].copy()
df = pd.concat([df, duplicates], ignore_index=True)

# 2. Missing email ~1.5%
email_null_idx = np.random.choice(df.index, size=int(len(df) * 0.015), replace=False)
df.loc[email_null_idx, "Email"] = None

# 3. Missing phone ~1.5%
phone_null_idx = np.random.choice(df.index, size=int(len(df) * 0.015), replace=False)
df.loc[phone_null_idx, "Phone"] = None

# 4. Bad date logic: ModifiedDate before CreatedDate ~1%
bad_date_idx = np.random.choice(df.index, size=int(len(df) * 0.01), replace=False)
df.loc[bad_date_idx, "ModifiedDate"] = df.loc[bad_date_idx, "CreatedDate"] - pd.Timedelta(days=30)

# 5. Inconsistent casing on Email and City ~1.5%
case_idx = np.random.choice(df.index, size=int(len(df) * 0.015), replace=False)
df.loc[case_idx, "Email"] = df.loc[case_idx, "Email"].str.upper()

# 6. Whitespace padding on FirstName/LastName ~1%
ws_idx = np.random.choice(df.index, size=int(len(df) * 0.01), replace=False)
df.loc[ws_idx, "FirstName"] = "  " + df.loc[ws_idx, "FirstName"] + "  "

# 7. Invalid email format (strip the @domain part) ~1%
bad_email_idx = np.random.choice(df.index, size=int(len(df) * 0.01), replace=False)
df.loc[bad_email_idx, "Email"] = df.loc[bad_email_idx, "Email"].str.split("@").str[0]

# 8. Inconsistent Status values ~1%
status_idx = np.random.choice(df.index, size=int(len(df) * 0.01), replace=False)
df.loc[status_idx, "Status"] = np.random.choice(["ACTIVE", "active", "A", "InActive"], size=len(status_idx))

print(df.shape)
print(df.head())
print(df.shape)
df.to_csv("customers_raw.csv", index=False)
print("Saved customers_raw.csv")