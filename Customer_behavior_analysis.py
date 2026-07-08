import pandas as pd
from sqlalchemy import create_engine
import urllib.parse

# -----------------------
# Load CSV
# -----------------------

df = pd.read_csv("customer_shopping_behavior.csv")

# -----------------------
# Missing Values
# -----------------------

df["Review Rating"] = (
    df.groupby("Category")["Review Rating"]
      .transform(lambda x: x.fillna(x.median()))
)

# -----------------------
# Rename Columns
# -----------------------

df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(" ", "_")
df = df.rename(columns={
    "purchase_amount_(usd)": "purchase_amount"
})

# -----------------------
# Age Group
# -----------------------

labels = [
    "Young Adult",
    "Adult",
    "Middle-aged",
    "Senior"
]

df["age_group"] = pd.qcut(
    df["age"],
    q=4,
    labels=labels
)

# -----------------------
# Purchase Frequency Days
# -----------------------

frequency_mapping = {
    "Fortnightly":14,
    "Weekly":7,
    "Monthly":30,
    "Quarterly":90,
    "Bi-Weekly":14,
    "Annually":365,
    "Every 3 Months":90
}

df["purchase_frequency_days"] = (
    df["frequency_of_purchases"]
      .map(frequency_mapping)
)

# -----------------------
# Drop Column
# -----------------------

df = df.drop("promo_code_used", axis=1)

# -----------------------
# MySQL Connection
# -----------------------

username = "root"
password = "Venkat@19"
host = "localhost"
port = "3306"
database = "customer_behavior"

password = urllib.parse.quote_plus(password)

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
)

# -----------------------
# Save to MySQL
# -----------------------

df.to_sql(
    "customer",
    engine,
    if_exists="replace",
    index=False
)

print("Data uploaded successfully!")

# -----------------------
# Read Data
# -----------------------

result = pd.read_sql(
    "SELECT * FROM customer LIMIT 5;",
    engine
)

print(result)