import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
np.random.seed(42)

# Load existing accounts so we only use valid AccountIDs
accounts_df = pd.read_csv("accounts_raw.csv")
valid_account_ids = accounts_df["AccountID"].unique()

num_transactions = 2000000

transaction_types = ["Debit", "Credit"]
statuses = ["Success", "Failed", "Pending"]

sampled_account_ids = np.random.choice(valid_account_ids, size=num_transactions, replace=True)
transaction_type_choices = np.random.choice(transaction_types, size=num_transactions, p=[0.6, 0.4])
status_choices = np.random.choice(statuses, size=num_transactions, p=[0.92, 0.05, 0.03])
amounts = np.round(np.random.uniform(10, 100000, size=num_transactions), 2)

transaction_dates = pd.to_datetime(
np.random.randint(
pd.Timestamp("2024-01-01").value // 10**9,
pd.Timestamp("2026-09-06").value // 10**9,
size=num_transactions
),
unit="s"
)

created_dates = transaction_dates
modified_dates = transaction_dates + pd.to_timedelta(np.random.randint(0, 3, size=num_transactions), unit="D")

df = pd.DataFrame({
"TransactionID": np.arange(1, num_transactions + 1),
"AccountID": sampled_account_ids,
"TransactionType": transaction_type_choices,
"Amount": amounts,
"TransactionDate": transaction_dates,
"Status": status_choices,
"CreatedDate": created_dates,
"ModifiedDate": modified_dates
})

n = len(df)

# Messiness injection

# 1. Negative amounts ~1%
neg_amt_idx = np.random.choice(df.index, size=int(n * 0.01), replace=False)
df.loc[neg_amt_idx, "Amount"] = -abs(df.loc[neg_amt_idx, "Amount"])

# 2. Zero amounts ~0.5%
zero_amt_idx = np.random.choice(df.index, size=int(n * 0.005), replace=False)
df.loc[zero_amt_idx, "Amount"] = 0

# 3. Missing TransactionDate ~1%
missing_date_idx = np.random.choice(df.index, size=int(n * 0.01), replace=False)
df.loc[missing_date_idx, "TransactionDate"] = pd.NaT

# 4. Duplicate transactions ~1%
dup_idx = np.random.choice(df.index, size=int(n * 0.01), replace=False)
duplicates = df.loc[dup_idx].copy()
df = pd.concat([df, duplicates], ignore_index=True)

# 5. Inconsistent casing on TransactionType/Status ~1%
casing_idx = np.random.choice(df.index, size=int(len(df) * 0.01), replace=False)
df.loc[casing_idx, "Status"] = df.loc[casing_idx, "Status"].str.upper()

print(df.shape)

df.to_csv("transactions_raw.csv", index=False)
print("Saved transactions_raw.csv")