import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
np.random.seed(42)

# Load existing customers so we only use valid CustomerIDs
customers_df = pd.read_csv("customers_raw.csv")
valid_customer_ids = customers_df["CustomerID"].unique()

num_accounts = 150000

account_types = ["Savings", "Current", "Fixed Deposit"]
statuses = ["Active", "Closed", "Dormant"]

accounts = []

# Randomly sample CustomerIDs WITH repetition, so some customers get multiple accounts
sampled_customer_ids = np.random.choice(valid_customer_ids, size=num_accounts, replace=True)

for i in range(num_accounts):
    account = {
        "AccountID": i + 1,
        "CustomerID": sampled_customer_ids[i],
        "AccountNumber": fake.unique.random_number(digits=12, fix_len=True),
        "AccountType": np.random.choice(account_types, p=[0.5, 0.35, 0.15]),
        "OpenDate": fake.date_between(start_date="-5y", end_date="-1y"),
        "Balance": round(np.random.uniform(0, 500000), 2),
        "Status": np.random.choice(statuses, p=[0.85, 0.10, 0.05]),
        "ModifiedDate": fake.date_between(start_date="-1y", end_date="today")
    }
    accounts.append(account)

df = pd.DataFrame(accounts)
n = len(df)

# 1. Negative balances ~1%
neg_balance_idx = np.random.choice(df.index, size=int(n * 0.01), replace=False)
df.loc[neg_balance_idx, "Balance"] = -abs(df.loc[neg_balance_idx, "Balance"])

# 2. ModifiedDate before OpenDate ~1%
bad_date_idx = np.random.choice(df.index, size=int(n * 0.01), replace=False)
df.loc[bad_date_idx, "ModifiedDate"] = pd.to_datetime(df.loc[bad_date_idx, "OpenDate"]) - pd.Timedelta(days=15)

# 3. Missing AccountNumber ~1%
missing_acc_num_idx = np.random.choice(df.index, size=int(n * 0.01), replace=False)
df.loc[missing_acc_num_idx, "AccountNumber"] = None

# 4. Missing AccountType ~1%
missing_type_idx = np.random.choice(df.index, size=int(n * 0.01), replace=False)
df.loc[missing_type_idx, "AccountType"] = None

# 5. Inconsistent casing on AccountType and Status ~1.5%
casing_idx = np.random.choice(df.index, size=int(n * 0.015), replace=False)
df.loc[casing_idx, "Status"] = df.loc[casing_idx, "Status"].str.upper()

print(df.shape)

df.to_csv("accounts_raw.csv", index=False)
print("Saved accounts_raw.csv")
print(df.head())
print(df.shape)